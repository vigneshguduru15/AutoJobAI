# matcher.py
def match_jobs(jobs, skills):
    """
    Score jobs based on overlap with extracted resume skills.
    Higher matching skill count = higher ranking.
    """
    if not jobs:
        return []

    skills = [s.lower() for s in skills]
    scored_jobs = []

    for job in jobs:
        desc = job.get("description", "").lower()
        title = job.get("title", "").lower()
        score = sum(1 for s in skills if s in desc or s in title)
        scored_jobs.append((score, job))

    # Sort by score (highest first)
    scored_jobs.sort(key=lambda x: x[0], reverse=True)

    return [job for score, job in scored_jobs]
