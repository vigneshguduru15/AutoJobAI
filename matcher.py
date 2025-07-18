# matcher.py
def match_jobs(resume_skills, jobs):
    matched_jobs = []

    for job in jobs:
        score = 0
        for skill in resume_skills:
            if skill.lower() in job.get("title", "").lower() or skill.lower() in job.get("description", "").lower():
                score += 1

        matched_jobs.append({
            "title": job.get("title", "No Title"),
            "location": job.get("location", "Unknown"),
            "description": job.get("description", ""),
            "apply_link": job.get("apply_link"),
            "score": score
        })

    matched_jobs.sort(key=lambda x: x["score"], reverse=True)
    return matched_jobs[:10] if matched_jobs else []
