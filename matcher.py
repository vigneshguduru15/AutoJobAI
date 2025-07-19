def match_jobs(jobs, skills):
    matched = []
    for job in jobs:
        title = job.get("title", "").lower()
        desc = job.get("description", "").lower()
        score = sum(skill.lower() in title or skill.lower() in desc for skill in skills)
        job["match_score"] = score
        matched.append(job)
    matched.sort(key=lambda x: x.get("match_score", 0), reverse=True)
    return matched
