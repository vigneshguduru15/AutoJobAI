from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_jobs(resume_text, jobs):
    if not resume_text or not jobs:
        return []

    descriptions = [resume_text] + [job["description"] for job in jobs]
    vectorizer = TfidfVectorizer().fit_transform(descriptions)
    similarity_scores = cosine_similarity(vectorizer[0:1], vectorizer[1:]).flatten()

    matched_jobs = []
    for idx, score in enumerate(similarity_scores):
        job = jobs[idx]
        matched_jobs.append({
            "title": job.get("title", "No title"),
            "link": job.get("link", ""),
            "apply_options": job.get("apply_options", []),
            "score": round(float(score), 2),
        })

    return sorted(matched_jobs, key=lambda x: x["score"], reverse=True)
