from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_jobs(resume_text, jobs):
    if not jobs:
        return []

    descriptions = [resume_text] + [job["description"] for job in jobs]
    vectorizer = TfidfVectorizer().fit_transform(descriptions)
    similarity = cosine_similarity(vectorizer[0:1], vectorizer[1:]).flatten()

    matched_jobs = []
    for i, score in enumerate(similarity):
        matched_jobs.append({
            "title": jobs[i]["title"],
            "link": jobs[i]["link"],
            "score": round(float(score), 2)
        })

    return sorted(matched_jobs, key=lambda x: x["score"], reverse=True)

