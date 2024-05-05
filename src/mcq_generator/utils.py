import os
import PyPDF2
import json
import traceback



def read_file(file):
    """
    Reads the contents of a file and returns them as a string.

    Parameters:
        file (file-like object): The file to be read.

    Returns:
        str: The contents of the file as a string.

    Raises:
        Exception: If there is an error reading the PDF file.
        Exception: If the file type is unsupported (only PDF and TXT are supported).
    """
    if file.name.endswith(".pdf"):
        try:
            pdfReader = PyPDF2.PdfFileReader(file)
            text = ""
            for page in pdfReader.pages:
                text += page.extractText()
            return text
        
        except Exception as e:
            raise Exception("Error reading the PDF file")
        
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception("Unsupported file type, only pdf and txt are supported")
    
def get_table_data(quiz_str):
    """
    Converts a string representation of a quiz to a list of dictionaries containing the MCQ questions, their options, and the correct answer.

    Args:
        quiz_str (str): A string representation of a quiz in JSON format.

    Returns:
        list: A list of dictionaries, where each dictionary represents a MCQ question and its options. The dictionaries have the following keys:
            - "MCQ" (str): The MCQ question.
            - "Choices" (str): The options for the MCQ question, formatted as "option1 -> value1 || option2 -> value2 || ...".
            - "Correct" (str): The correct answer for the MCQ question.

    Raises:
        Exception: If there is an error converting the string to a dictionary or if the quiz format is invalid.

    Example:
        >>> quiz_str = '{"question1": {"mcq": "What is the capital of France?", "options": {"Paris": "A", "London": "B", "Berlin": "C"}, "correct": "A"}, "question2": {"mcq": "What is the largest planet in our solar system?", "options": {"Earth": "A", "Saturn": "B", "Jupiter": "C"}, "correct": "B"}}'
        >>> get_table_data(quiz_str)
        [{'MCQ': 'What is the capital of France?', 'Choices': 'Paris -> A || London -> B || Berlin -> C', 'Correct': 'A'}, {'MCQ': 'What is the largest planet in our solar system?', 'Choices': 'Earth -> A || Saturn -> B || Jupiter -> C', 'Correct': 'B'}]
    """
    try:
        # convert the quiz from a string to a dictionary
        quiz_str =quiz_str.replace('\n','') # remove newlines
        quiz_dict =json.loads(quiz_str)
        quiz_table_data = []
        
       # Iterate through the dictionary and extract the required
        for key, value in quiz_dict.items():
            mcq = value['mcq']
            options = " || ".join(
                    [
                    f"{option} -> {option_value}" for option, option_value in value["options"].items()
                ]
            )
            
            correct = value["correct"]
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})
            
        return quiz_table_data
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False
    