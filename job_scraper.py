import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()

def get_jobs(role="python developer"):
    params = {
        "engine": "google_jobs",
        "q": role,
        "hl": "en",
        "api_key": os.getenv("SERPAPI_KEY")
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    jobs = []
    for job in results.get("jobs_results", []):
        jobs.append({
            "title": job.get("title", "No Title"),
            "link": job.get("apply_options", [{}])[0].get("link", "#")
        })

    return jobs
