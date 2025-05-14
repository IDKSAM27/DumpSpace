# Step 1: Install necessary libraries 
 
# Step 2: Import the required modules 
from langchain.llms import Cohere 
from langchain.prompts import PromptTemplate 
from langchain import LLMChain 
# from google.colab import drive 
 
# Step 3: Mount Google Drive to access the document 
# drive.mount('/content/drive') 
 
# Step 4: Load the text document from Google Drive 
file_path = "utils/sample_text.txt"  # Change this path to your file location 
with open(file_path, "r") as file: 
    text = file.read() 
 
# Step 5: Set up Cohere API key 
cohere_api_key = "YOUR_COHERE_API_KEY"  # Replace with your actual Cohere API key 
 
# Step 6: Create a prompt template 
prompt_template = """ 
Summarize the following text in three bullet points: 
{text} 
""" 
 
# Step 7: Configure the Cohere model with Langchain 
llm = Cohere(cohere_api_key=cohere_api_key) 
prompt = PromptTemplate(input_variables=["text"], template=prompt_template) 
 
# Step 8: Create an LLMChain with the Cohere model and prompt template 
chain = LLMChain(llm=llm, prompt=prompt) 
 
# Step 9: Run the chain on the loaded text 
result = chain.run(text) 
 
# Step 10: Display the formatted output 
print("Summarized Output in Bullet Points:") 
print(result) 