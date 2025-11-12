from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import nltk

nltk.download('punkt')

# Load semantic similarity model
s_model = SentenceTransformer('all-MiniLM-L6-v2')

def sentence_similarity_score(student_text, reference_texts):
    sentences = nltk.sent_tokenize(student_text)

    plagiarised_count = 0
    scores = []
    
    # Encode reference corpus
    ref_embeddings = s_model.encode(reference_texts, convert_to_tensor=True)

    for sent in sentences:
        sent_emb = s_model.encode(sent, convert_to_tensor=True)
        
        # Compute cosine similarity with reference
        cosine_scores = util.cos_sim(sent_emb, ref_embeddings)[0]
        
        max_score = float(cosine_scores.max().item())
        scores.append(max_score)
        
        if max_score > 0.80:  # threshold for plagiarism
            plagiarised_count += 1

    plagiarism_percentage = (plagiarised_count / len(sentences)) * 100
    
    return plagiarism_percentage, scores


print("END OF FILE BITCHHHHH")



def tfidf_plagiarism_score(student_text, reference_texts):
    texts = [student_text] + reference_texts
    vectorizer = TfidfVectorizer().fit(texts)
    vectors = vectorizer.transform(texts)
    
    student_vec = vectors[0]
    ref_vecs = vectors[1:]
    
    cosine_similarities = (student_vec @ ref_vecs.T).toarray()[0]
    max_sim = max(cosine_similarities)
    
    exact_match_percentage = max_sim * 100
    return exact_match_percentage




def combined_plagiarism_score(student_text, reference_texts):
    sem_perc, sem_scores = sentence_similarity_score(student_text, reference_texts)
    tfidf_perc = tfidf_plagiarism_score(student_text, reference_texts)

    # Weighted system
    # 60% semantic similarity, 40% exact match
    a = (0.8 * sem_perc)
    b = (0.4 * tfidf_perc)
    final_score =  a+b

    return {
        "semantic_percentage": float(sem_perc),
        "exact_match_percentage": float(tfidf_perc),
        "final_plagiarism_score": float(final_score)
    }


reference_texts = []
for i in range(1, 4):
    with open(f"bottom_text/ref{i}.txt", encoding="utf-8") as f:
        reference_texts.append(f.read())

with open("student/student.txt", encoding="utf-8") as f:
    student_text = f.read()

result = combined_plagiarism_score(student_text, reference_texts)
print(result)
