'''
7. Summarize long texts using a pre-trained summarization model using Hugging face model.
Load the summarization pipeline. Take a passage as input and obtain the summarized text.
'''

# Step 1: Import the Hugging Face pipeline 
from transformers import pipeline 
 
# Step 2: Load the summarization pipeline 
summarizer = pipeline("summarization") 
 
# Step 3: Input a long passage for summarization 
long_text = """ 
Artificial Intelligence (AI) is transforming various industries by automating tasks, improving 
efficiency,  
and enabling new capabilities. In the healthcare sector, AI is used for disease diagnosis, 
personalized medicine,  
and drug discovery. In the business world, AI-powered systems are optimizing customer 
service, fraud detection,  
and supply chain management. AI's impact on everyday life is significant, from smart 
assistants to recommendation  
systems in streaming platforms. As AI continues to evolve, it promises even greater 
advancements in fields like  
education, transportation, and environmental sustainability. 
""" 
 
# Step 4: Summarize the input passage 
summary = summarizer(long_text, max_length=50, min_length=20, 
do_sample=False)[0]["summary_text"] 
 
# Step 5: Print the summarized text 
print("Summarized Text:") 
print(summary)