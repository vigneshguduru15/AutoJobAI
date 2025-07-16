from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def rank_jobs(resume_text, jobs):
    if not jobs:
        return []

    descriptions = [resume_text] + [job["description"] for job in jobs]
    vectorizer = TfidfVectorizer().fit_transform(descriptions)
    similarity = cosine_similarity(vectorizer[0:1], vectorizer[1:]).flatten()

    matched_jobs = []
    for i, score in enumerate(similarity):
        job = jobs[i]
        link = job.get("apply_options", [{}])[0].get("link", "⚠️ No link available")
        matched_jobs.append({
            "title": job.get("title", "Untitled"),
            "link": link,
            "score": round(float(score), 2)
        })

    return sorted(matched_jobs, key=lambda x: x["score"], reverse=True)
