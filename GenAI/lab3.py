'''
3. Train a custom Word2Vec model on a small dataset. Train embeddings on a domain-specific corpus
and analyze how embeddings capture domain-specific semantics
'''

from gensim.models import Word2Vec 
 
medical_data = [ 
    ["patient", "doctor", "nurse", "hospital", "treatment"], 
    ["cancer", "chemotherapy", "radiation", "surgery", "recovery"], 
    ["infection", "antibiotics", "diagnosis", "disease", "virus"], 
    ["heart", "disease", "surgery", "cardiology", "recovery"] ] 
 
model = Word2Vec(sentences=medical_data, vector_size=10, window=2, min_count=1, workers=1, epochs=50) 
 
input_word = "patient" 
if input_word in model.wv: 
    similar_words = model.wv.most_similar(input_word, topn=3) 
    print(f"3 words similar to '{input_word}':") 
    for word, similarity in similar_words: 
        print(f"{word} (similarity: {similarity:.2f})") 
else: 
    print(f"'{input_word}' is not in the vocabulary.") 