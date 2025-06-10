'''
1. Explore pre-trained word vectors. Explore word relationships using vector arithmetic.
Perform arithmetic operations and analyze results.
'''
 
from gensim.downloader import load 
word_vectors = load('glove-wiki-gigaword-100')  # Automatically downloads the model 
 
result = word_vectors.most_similar(positive=['kitten', 'dog'], negative=['cat'], topn=1) 
print("Result of 'kitten - cat + dog':", result[0][0])  # Expected output: 'puppy' or a related word 
 
result = word_vectors.most_similar(positive=['orange', 'tropical'], negative=['fruit'], topn=1) 
print("Result of 'orange - fruit + tropical':", result[0][0])  # Expected output: 'mango' or a related word 