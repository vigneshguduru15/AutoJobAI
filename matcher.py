def match_jobs(jobs, skills):
    """Score jobs by overlap with extracted skills."""
    matched = []
    for job in jobs:
        score = 0
        desc = (job.get("description") or "").lower()
        title = (job.get("title") or "").lower()

        for skill in skills:
            if skill.lower() in desc or skill.lower() in title:
                score += 1

        job["match_score"] = score
        matched.append(job)

    return sorted(matched, key=lambda x: x["match_score"], reverse=True)
    return matched