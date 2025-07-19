def match_jobs(jobs, skills):
    """Simple skill-based job ranking."""
    if not skills:
        return jobs
    scored = []
    for job in jobs:
        desc = (job.get("description") or "").lower()
        score = sum(1 for skill in skills if skill.lower() in desc)
        scored.append((score, job))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [job for _, job in scored]
