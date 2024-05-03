# find_packages is used to find all the packages in the project locally
#setup is used to set up the project
#setuptools is used to install the packages

from setuptools import setup, find_packages 

setup(
    name='mcq_generator',
    version='0.0.1',
    author='Oazed',
    author_email='oazedlium@gmail.com',
    install_requires=[
        'openai',
        'langchain',
        'streamlit',
        'python-dotenv',
        'PyPDF2' 
    ],
    packages=find_packages(),
)