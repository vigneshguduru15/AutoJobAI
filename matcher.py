from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_jobs(skills, jobs, top_n=10):
    if not jobs:
        return []

    skill_text = ' '.join(skills).lower()

    job_texts = []
    for job in jobs:
        content = f"{job.get('title', '')} {job.get('description', '')}".lower()
        job_texts.append(content)

    vectorizer = TfidfVectorizer().fit([skill_text] + job_texts)
    vectors = vectorizer.transform([skill_text] + job_texts)

    similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()

    scored_jobs = []
    for job, score in zip(jobs, similarities):
        job['score'] = score
        scored_jobs.append(job)

    scored_jobs.sort(key=lambda x: x['score'], reverse=True)
    return scored_jobs[:top_n]

