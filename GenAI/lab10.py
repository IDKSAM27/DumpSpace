'''
10. Build a chatbot for the Indian Penal Code. We'll start by downloading the official Indian Penal Code 
document, and then we'll create a chatbot that can interact with it. Users will be able to ask questions 
about the Indian Penal Code and have a conversation with it.
'''

from langchain.chains import load_qa_chain 
from langchain.docstore.document import Document 
from langchain.llms import OpenAI 
 
ipc_file_path = "path_to_your_ipc_file.txt"  # Replace with the actual path to your IPC text file 
 
with open(ipc_file_path, "r", encoding="utf-8") as file: 
    ipc_text = file.read() 
 
ipc_document = Document(page_content=ipc_text) 
 
llm = OpenAI(openai_api_key="s8BZSruqi05azWhXqqk1flxfeBWInUbH1sVBDb1m", temperature=0.3)  # Use temperature=0.3 for more factual responses 
 
qa_chain = load_qa_chain(llm, chain_type="stuff") 
 
print("Chatbot for the Indian Penal Code (IPC)") 
print("Ask a question about the Indian Penal Code (type 'exit' to stop):") 
 
while True: 
    user_question = input("\nYour question: ") 
    if user_question.lower() == "exit": 
        print("Goodbye!") 
        break 
 
    response = qa_chain.run(input_documents=[ipc_document], question=user_question) 
    print(f"Answer: {response}") 