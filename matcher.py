from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_jobs(resume_text, jobs):
    if not jobs:
        return []

    descriptions = [resume_text] + [job.get("description", "") for job in jobs]
    vectorizer = TfidfVectorizer().fit_transform(descriptions)
    similarity = cosine_similarity(vectorizer[0:1], vectorizer[1:]).flatten()

    matched_jobs = []

    for i, score in enumerate(similarity):
        job = jobs[i]

        # Step 1: Try apply_options
        link = None
        if "apply_options" in job and isinstance(job["apply_options"], list):
            for option in job["apply_options"]:
                if "link" in option and option["link"].startswith("http"):
                    link = option["link"]
                    break

        # Step 2: Fallback to share_link
        if not link and job.get("share_link", "").startswith("http"):
            link = job["share_link"]

        if not link:
            print("⚠️ Invalid job link found. Skipping this job.")
            continue

        matched_jobs.append({
            "title": job.get("title", "Untitled"),
            "link": link,
            "score": round(float(score), 2)
        })

    return sorted(matched_jobs, key=lambda x: x["score"], reverse=True)
