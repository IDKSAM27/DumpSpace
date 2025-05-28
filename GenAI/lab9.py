# Step 1: Install necessary libraries 
# pip install langchain pydantic wikipedia-api 
 
# Step 2: Import required modules 
from langchain.llms import Cohere 
from langchain.prompts import PromptTemplate 
from langchain import LLMChain 
from pydantic import BaseModel 
import wikipediaapi 
 
# Step 3: Define a Pydantic schema for the institution's details 
class InstitutionDetails(BaseModel): 
    founder: str 
    founded: str 
    branches: str 
    employees: str 
    summary: str 
 
# Step 4: Function to fetch details from Wikipedia with user-agent specified 
def fetch_wikipedia_summary(institution_name): 
    wiki_wiki = wikipediaapi.Wikipedia(language='en', 
user_agent="InstitutionInfoBot/1.0 (contact: youremail@example.com)") 
    page = wiki_wiki.page(institution_name) 
    if page.exists(): 
        return page.text 
    else: 
        return "No information available on Wikipedia for this institution." 
# Step 5: Prompt template for extracting relevant details 
prompt_template = """ 
Extract the following information from the given text: - Founder - Founded (year) - Current branches - Number of employees - 4-line brief summary 
Text: {text} 
Provide the information in the following format: 
Founder: <founder> 
Founded: <founded> 
Branches: <branches> 
Employees: <employees> 
Summary: <summary> 
""" 
 
# Step 6: Take institution name as input 
institution_name = input("Enter the name of the institution: ") 
 
# Step 7: Fetch Wikipedia data for the institution 
wiki_text = fetch_wikipedia_summary(institution_name) 
 
# Step 8: Set up Cohere (Replace YOUR_COHERE_API_KEY with your actual key) 
cohere_api_key = "YOUR_COHERE_API_KEY" 
llm = Cohere(cohere_api_key=cohere_api_key) 
 
# Step 9: Create the Langchain prompt and chain 
prompt = PromptTemplate(input_variables=["text"], template=prompt_template) 
chain = LLMChain(llm=llm, prompt=prompt) 
 
# Step 10: Run the chain and parse the output 
response = chain.run(wiki_text) 
 
# Step 11: Parse the response using Pydantic 
try: 
    details = InstitutionDetails.parse_raw(response) 
    print("Institution Details:") 
    print(f"Founder: {details.founder}") 
    print(f"Founded: {details.founded}") 
    print(f"Branches: {details.branches}") 
    print(f"Employees: {details.employees}") 
    print(f"Summary: {details.summary}") 
except Exception as e: 
    print("Error parsing the response:", e) 