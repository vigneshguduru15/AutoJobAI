from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def rank_jobs(resume_text, jobs):
    texts = [resume_text] + [job["title"] for job in jobs]
    vec = TfidfVectorizer().fit_transform(texts)

    sim = cosine_similarity(vec[0:1], vec[1:]).flatten()
    ranked = sorted(zip(jobs, sim), key=lambda x: x[1], reverse=True)

    return ranked
