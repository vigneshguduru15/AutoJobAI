def match_jobs(jobs, skills):
    """Rank jobs based on skill matches."""
    ranked = []
    skill_set = set(skill.lower() for skill in skills)

    for job in jobs:
        text = (
            (job.get("title", "") or "") + " " +
            (job.get("description", "") or "")
        ).lower()
        score = sum(1 for skill in skill_set if skill in text)
        ranked.append((score, job))

    ranked.sort(key=lambda x: x[0], reverse=True)
    return [job for score, job in ranked]
