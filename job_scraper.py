import os
from serpapi import GoogleSearch
from dotenv import load_dotenv
load_dotenv()

SERP_API_KEY = os.getenv("SERPAPI_API_KEY")

def get_jobs(query="software engineer", location="India", num_jobs=20):
    if not SERP_API_KEY:
        return []

    params = {
        "engine": "google_jobs",
        "q": query,
        "location": location,
        "api_key": SERP_API_KEY
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        jobs = results.get("jobs_results", [])
        formatted_jobs = []

        for job in jobs[:num_jobs]:
            if "title" in job and "company_name" in job and "job_id" in job:
                link = job.get("related_links", [{}])[0].get("link") or job.get("job_highlights", [{}])[0].get("link")
                link = link or job.get("via") or "#"
                formatted_jobs.append({
                    "title": job.get("title"),
                    "company": job.get("company_name"),
                    "description": job.get("description", ""),
                    "location": job.get("location", "Remote"),
                    "link": link
                })
        return formatted_jobs
    except Exception as e:
        print("Error fetching jobs:", e)
        return []
