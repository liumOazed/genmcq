import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from src.mcq_generator.utils import read_file, get_table_data
from src.mcq_generator.logger import logging
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcq_generator.MCQgen import generate_evaluate_chain

# Loading json file using absolute path
with open('C:\genmcq\Response.json') as file:
    RESPONSE_JSON = json.load(file)
    
# Creating a title for the app
st.title('MCQ Generator with Langchain and OpenAI')

# Creating a form using st.form
with st.form('user_inputs'):
    # File upload
    uploaded_file = st.file_uploader("Upload a PDF/Text File", type=['pdf', 'txt']) 
    
    # Input Fields
    mcq_count = st.number_input('Number of MCQ questions', min_value=3, max_value=10)  
    
    # Subject drop down
    subject_options = ['English Literature', 'mathematics', 'Kids riddle', 'history']
    subject_dropdown = st.selectbox('Subject', subject_options)
    #subject = st.text_input('Subject', max_chars=20) 
    
    # Quiz tone
    complexity_level = st.selectbox('Complexity Level', ('Easy', 'Medium', 'Advanced'))
    #tone = st.text_input('Complexity Level', max_chars=20, placeholder='Simple')
    
    # Add Button
    button = st.form_submit_button(label='Generate MCQs')
    
    if button and uploaded_file is not None and mcq_count and subject_dropdown and complexity_level:
        with st.spinner('Generating MCQs...'):
            try:
                text = read_file(uploaded_file)
                # Count tokens and cost of API call
                with get_openai_callback() as cb:
                    response=generate_evaluate_chain(
                        {
                            'text': text,
                            'number': mcq_count,
                            'subject': subject_dropdown,
                            'tone': complexity_level,
                            'response_json': json.dumps(RESPONSE_JSON)
                        }
                    )
                    
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")
                
            else:
                print(f"Total Tokens: {cb.total_tokens}")
                print(f"Prompt Tokens: {cb.prompt_tokens}")
                print(f"Completion Tokens: {cb.completion_tokens}")
                print(f"Total Cost: ${cb.total_cost}")
                
                if isinstance(response, dict):
                    # Extract the quiz data from response
                    quiz = response.get('quiz',None)
                    if quiz is not None:
                        table_data= get_table_data(quiz)
                        if table_data is not None:
                            df= pd.DataFrame(table_data)
                            df.index= df.index+1
                            st.table(df)
                            # Display the review in a text bos
                            st.text_area(label="Review", value=response['review'])
                        else:
                            st.error("Error in the table data")
                            
                else:
                    st.write(response)
                            