'''
5. Use word embeddings to create meaningful sentences for creative tasks. Retrieve similar words for a seed word.
Create a sentence or story using these words as a starting point. Write a program that:
Takes a seed word. Generate similar words. Cosntructs a short paragraph using these words.
'''

# Step 1: Pre-defined dictionary of words and their similar terms 
word_embeddings = { 
    "adventure": ["journey", "exploration", "quest"], 
    "robot": ["machine", "automation", "mechanism"], 
    "forest": ["woods", "jungle", "wilderness"], 
    "ocean": ["sea", "waves", "depths"], 
    "magic": ["spell", "wizardry", "enchantment"] 
} 
 
# Step 2: Function to get similar words for a seed word 
def get_similar_words(seed_word): 
    if seed_word in word_embeddings: 
        return word_embeddings[seed_word] 
    else: 
        return ["No similar words found"] 
 
# Step 3: Function to create a short paragraph using the seed word and similar words 
def create_paragraph(seed_word): 
    similar_words = get_similar_words(seed_word) 
    if "No similar words found" in similar_words: 
        return f"Sorry, I couldn't find similar words for '{seed_word}'." 
     
    # Construct a short story using the seed word and similar words 
    paragraph = ( 
        f"Once upon a time, there was a great {seed_word}. " 
        f"It was full of {', '.join(similar_words[:-1])}, and {similar_words[-1]}. " 
        f"Everyone who experienced this {seed_word} always remembered it as a remarkable tale." 
    ) 
    return paragraph 
 
# Step 4: Input a seed word 
seed_word = "adventure"  # You can change this to "robot", "forest", "ocean", "magic", etc. 
 
# Step 5: Generate and print the paragraph 
story = create_paragraph(seed_word) 
print("Generated Paragraph:") 
print(story)