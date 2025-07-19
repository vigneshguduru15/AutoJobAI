import re

def normalize_text(text):
    """Lowercase and clean text for matching."""
    return re.sub(r"[^a-z0-9\s]", "", text.lower())

def match_jobs(jobs, skills):
    """Rank jobs by number of matching skills."""
    normalized_skills = [normalize_text(skill) for skill in skills]
    ranked = []

    for job in jobs:
        title = normalize_text(job.get("title", ""))
        desc = normalize_text(job.get("description", ""))
        company = normalize_text(job.get("company_name", ""))

        score = sum(skill in title or skill in desc or skill in company for skill in normalized_skills)
        ranked.append((score, job))

    ranked.sort(key=lambda x: x[0], reverse=True)
    return [job for score, job in ranked]
