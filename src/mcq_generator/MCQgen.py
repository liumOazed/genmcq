import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from src.mcq_generator.utils import read_file, get_table_data
from src.mcq_generator.logger import logging
import PyPDF2

from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain 

# Load environment variables from .env file
load_dotenv()
# Access the API key from the environment variable just like you would qith os.environ
KEY = os.getenv("OPENAI_API_KEY")
print(KEY)

# Set up the OpenAI LLM
llm = ChatOpenAI(openai_api_key=KEY, model_name="gpt-3.5-turbo", temperature=0.7) 

# Setting up the input prompt (few-shot example)
TEMPLATE = """
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}

"""
# Creating object of the PromptTemplate class
quiz_gen_prompt = PromptTemplate(
    input_variables=["text","number", "subject","tone", "response_json"], # Variables user will pass in the prompt
    template = TEMPLATE     
)

# Now I will create LLM Chain. LLM chain is used to connect multiple components together.
# Here the 2 components are PromptTemplate and LLM.
quiz_chain = LLMChain(llm=llm, prompt=quiz_gen_prompt, output_key="quiz", verbose=True)

# This prompt is regarding to the evaluation of the quiz
TEMPLATE_2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""
# Creating object of the 2nd PromptTemplate class this will quiz evaluation
quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", "quiz"], template=TEMPLATE)

# Second Chain
review_chain=LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

# Setting up the Sequential Chain by using both chains
generate_evaluate_chain=SequentialChain(chains=[quiz_chain, review_chain], input_variables=["text", "number", "subject", "tone", "response_json"],
                                        output_variables=["quiz", "review"], verbose=True)