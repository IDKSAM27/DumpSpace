'''
8. Install langchain, cohere, langchain-community. Get the api key. Load a text document from your google drive.
Create a prompt template to display the output in a particular manner.
'''

from langchain.llms import Cohere
from langchain.prompts import PromptTemplate
from langchain import LLMChain
from google.colab import drive

drive.mount('/content/drive')

file_path = "/content/drive/MyDrive/Text/crow.txt"
with open(file_path, "r") as file:
    text = file.read()

cohere_api_key = "xNBCmAElkHo9M2tjr6d3SLP80NbMt8MofoUMsREE"

prompt_template = """
Summarize the following text in two bullet points:
{text}
"""

llm = Cohere(cohere_api_key=cohere_api_key)
prompt = PromptTemplate(input_variables=["text"], template=prompt_template)

chain = LLMChain(llm=llm, prompt=prompt)

result = chain.run(text)

print(text)
print("Summarized Output in Bullet Points:")
print(result)



# Import required libraries
from langchain.llms import Cohere
from langchain.prompts import PromptTemplate
from langchain import LLMChain

# Hardcoded API Key (only for local testing – avoid in production)
cohere_api_key = "xNBCmAElkHo9M2tjr6d3SLP80NbMt8MofoUMsREE"

# Update this to match the local file path on your system
file_path = "C:/Users/YourUsername/Documents/crow.txt"  # <- Replace with your actual path

# Read the text file
with open(file_path, "r") as file:
    text = file.read()

# Prompt template
prompt_template = """
Summarize the following text in two bullet points:
{text}
"""

# Set up LangChain components
llm = Cohere(cohere_api_key=cohere_api_key)
prompt = PromptTemplate(input_variables=["text"], template=prompt_template)
chain = LLMChain(llm=llm, prompt=prompt)

# Generate summary
result = chain.run(text)

# Print results
print("Original Text:")
print(text)
print("\nSummarized Output in Bullet Points:")
print(result)
