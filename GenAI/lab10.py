'''
10. Build a chatbot for the Indian Penal Code. We'll start by downloading the official Indian Penal Code 
document, and then we'll create a chatbot that can interact with it. Users will be able to ask questions 
about the Indian Penal Code and have a conversation with it.
'''

# Step 1: Install necessary packages 
# !pip install langchain pydantic wikipedia-api openai 
 
# Step 2: Import required modules 
from langchain.chains import load_qa_chain 
from langchain.docstore.document import Document 
from langchain.llms import OpenAI 
 
# Step 3: Load the Indian Penal Code text from a file 
ipc_file_path = "path_to_your_ipc_file.txt"  # Replace with the actual path to your IPC text file 
 
# Read the IPC document 
with open(ipc_file_path, "r", encoding="utf-8") as file: 
    ipc_text = file.read() 
 
# Step 4: Create a Langchain Document object 
ipc_document = Document(page_content=ipc_text) 
 
# Step 5: Set up OpenAI (or any other LLM of your choice) 
llm = OpenAI(openai_api_key="YOUR_OPENAI_API_KEY", temperature=0.3)  # Use temperature=0.3 for more factual responses 
 
# Step 6: Create a simple question-answering chain 
qa_chain = load_qa_chain(llm, chain_type="stuff") 
 
# Step 7: Chat with the chatbot 
print("Chatbot for the Indian Penal Code (IPC)") 
print("Ask a question about the Indian Penal Code (type 'exit' to stop):") 
 
while True: 
    user_question = input("\nYour question: ") 
    if user_question.lower() == "exit": 
        print("Goodbye!") 
        break 
 
    # Use the QA chain to answer the question 
    response = qa_chain.run(input_documents=[ipc_document], question=user_question) 
    print(f"Answer: {response}") 