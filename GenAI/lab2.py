'''
2. Use dimensionality reduction to visualize word embeddings for Q1
Select 10 words from a specific domain and visualize their embeddings. Analyze clusters and relationships
Generate contextually rich outputs using embeddings.
Write a program to generate 5 semantically similar words for a given input.
'''

import matplotlib.pyplot as plt 
from sklearn.manifold import TSNE 
from gensim.downloader import load 
import numpy as np  # Import NumPy for array conversion 
 
# Load pre-trained word vectors (GloVe - 100 dimensions) 
word_vectors = load('glove-wiki-gigaword-100') 
 
# Select 10 words from the "technology" domain (ensure words exist in the model) 
tech_words = ['computer', 'internet', 'software', 'hardware', 'network', 'data', 'cloud', 'robot', 
'algorithm', 'technology'] 
tech_words = [word for word in tech_words if word in word_vectors.key_to_index] 
 
# Extract word vectors and convert to a NumPy array 
vectors = np.array([word_vectors[word] for word in tech_words]) 
 
# Reduce dimensions using t-SNE 
tsne = TSNE(n_components=2, random_state=42, perplexity=5)  # Perplexity is reduced to match the small sample size 
reduced_vectors = tsne.fit_transform(vectors) 
 
# Plot the 2D visualization 
plt.figure(figsize=(10, 6)) 
for i, word in enumerate(tech_words): 
    plt.scatter(reduced_vectors[i, 0], reduced_vectors[i, 1], label=word) 
    plt.text(reduced_vectors[i, 0] + 0.02, reduced_vectors[i, 1] + 0.02, word, fontsize=12) 
plt.title("t-SNE Visualization of Technology Words") 
plt.xlabel("Dimension 1") 
plt.ylabel("Dimension 2") 
plt.legend() 
plt.show() 
 
# Generate 5 semantically similar words for a given input word 
input_word = 'computer' 
if input_word in word_vectors.key_to_index: 
    similar_words = word_vectors.most_similar(input_word, topn=5) 
    print(f"5 words similar to '{input_word}':") 
    for word, similarity in similar_words: 
        print(f"{word} (similarity: {similarity:.2f})") 
else: 
    print(f"'{input_word}' is not in the vocabulary.")