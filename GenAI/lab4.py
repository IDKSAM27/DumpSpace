'''
4. Use word embeddings to improve prompts for Generative AI model.
Retrieve similar words using word embeddings. Use the similar words to enrich a
GenAI prompt. Use the AI model to generate responses for the original and enriched prompts. Compare the outputs in terms of
details and relevance
'''

# Step 1: Pre-defined dictionary of words and their similar terms (static word embeddings) 
word_embeddings = { 
    "ai": ["machine learning", "deep learning", "data science"], 
    "data": ["information", "dataset", "analytics"], 
    "science": ["research", "experiment", "technology"], 
    "learning": ["education", "training", "knowledge"], 
    "robot": ["automation", "machine", "mechanism"] 
} 
 
# Step 2: Function to find similar words using the static dictionary 
def find_similar_words(word): 
    if word in word_embeddings: 
        return word_embeddings[word] 
    else: 
        return [] 
 
# Step 3: Function to enrich a prompt with similar words 
def enrich_prompt(prompt): 
    words = prompt.lower().split() 
    enriched_words = [] 
    for word in words: 
        similar_words = find_similar_words(word) 
        if similar_words: 
            enriched_words.append(f"{word} ({', '.join(similar_words)})") 
        else: 
            enriched_words.append(word) 
    return " ".join(enriched_words) 
 
# Step 4: Original prompt 
original_prompt = "Explain AI and its applications in science." 
 
# Step 5: Enrich the prompt using similar words 
enriched_prompt = enrich_prompt(original_prompt) 
 
# Step 6: Print the original and enriched prompts 
print("Original Prompt:") 
print(original_prompt) 
print("\nEnriched Prompt:") 
print(enriched_prompt) 