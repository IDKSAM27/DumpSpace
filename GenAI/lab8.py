'''
8. Install langchain, cohere, langchain-community. Get the api key. Load a text document from your google drive.
Create a prompt template to display the output in a particular manner.
'''

'''
from langchain.llms import Cohere
from langchain.prompts import PromptTemplate
from langchain import LLMChain
from google.colab import drive

drive.mount('/content/drive')

file_path = "/content/drive/MyDrive/Text/crow.txt"
with open(file_path, "r") as file:
    text = file.read()

cohere_api_key = ""

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
'''

from langchain.llms import Cohere
from langchain.prompts import PromptTemplate
from langchain import LLMChain

cohere_api_key = ""

file_path = "D:/Code_dumpspace/GenAI/utils/sample_text.txt"  

with open(file_path, "r") as file:
    text = file.read()

prompt_template = """
Summarize the following text in two bullet points:
{text}
"""

llm = Cohere(cohere_api_key=cohere_api_key)
prompt = PromptTemplate(input_variables=["text"], template=prompt_template)
chain = LLMChain(llm=llm, prompt=prompt)

result = chain.run(text)

print("Original Text:")
print(text)
print("\nSummarized Output in Bullet Points:")
print(result)
