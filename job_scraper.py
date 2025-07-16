import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()

def get_jobs(role, location="India", num_jobs=10):
    params = {
        "engine": "google_jobs",
        "q": role,
        "location": location,
        "api_key": os.getenv("SERPAPI_API_KEY"),
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    jobs = []
    for job in results.get("jobs_results", []):
        title = job.get("title")
        link = job.get("related_links", [{}])[0].get("link") or job.get("apply_options", [{}])[0].get("link") or job.get("job_id")
        description = job.get("description")

        # Skip if link or description is missing
        if not link or not description:
            print("⚠️ Invalid job link or description. Skipping this job.")
            continue

        jobs.append({
            "title": title,
            "link": link if link.startswith("http") else f"https://www.google.com/search?q={role}+{location}",
            "description": description
        })

    return jobs
