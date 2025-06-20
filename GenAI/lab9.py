'''
9. Take the institution name as input. Use pydantic to define the schema for the desired output and create custom
output parser. Invoke the Chain and Fetch Results. Extract the below Institution related details from Wikipedia:
The founder of the Institution.
When it was founded.
The current branches in the institution.
How many employees  are working in it.
A brief 4-line summary of the institution.
'''

from langchain.llms import Cohere 
from langchain.prompts import PromptTemplate 
from langchain import LLMChain 
from pydantic import BaseModel 
import wikipediaapi 
 
class InstitutionDetails(BaseModel): 
    founder: str 
    founded: str 
    branches: str 
    employees: str 
    summary: str 
 
def fetch_wikipedia_summary(institution_name): 
    wiki_wiki = wikipediaapi.Wikipedia(language='en', 
user_agent="InstitutionInfoBot/1.0 (contact: youremail@example.com)") 
    page = wiki_wiki.page(institution_name) 
    if page.exists(): 
        return page.text 
    else: 
        return "No information available on Wikipedia for this institution." 

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
 
institution_name = input("Enter the name of the institution: ") 
 
wiki_text = fetch_wikipedia_summary(institution_name) 
 
cohere_api_key = "" 
llm = Cohere(cohere_api_key=cohere_api_key) 
 
prompt = PromptTemplate(input_variables=["text"], template=prompt_template) 
chain = LLMChain(llm=llm, prompt=prompt) 
 
response = chain.run(wiki_text) 
 
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