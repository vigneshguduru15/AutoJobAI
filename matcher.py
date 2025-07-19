# matcher.py
def match_jobs(jobs, skills):
    """
    Match jobs based on overlap with extracted skills.
    Returns jobs sorted by relevance (highest matches first).
    """
    if not jobs or not skills:
        return jobs  # Return as-is if no skills to match

    skill_set = set(skill.lower() for skill in skills)

    # Add a "match_score" to each job based on skill overlap
    for job in jobs:
        text = f"{job.get('title', '')} {job.get('description', '')}".lower()
        job["match_score"] = sum(1 for skill in skill_set if skill in text)

    # Sort by match_score (descending)
    matched = sorted(jobs, key=lambda x: x.get("match_score", 0), reverse=True)
    return matched
