import os
import requests

def get_jobs(role="python developer", location="India", num_results=10):
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise ValueError("SERPAPI_API_KEY not found in environment")

    params = {
        "engine": "google_jobs",
        "q": role,
        "location": location,
        "api_key": api_key
    }

    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()

    jobs = []
    results = data.get("jobs_results", [])[:num_results]

    for result in results:
        jobs.append({
            "title": result.get("title", "No Title"),
            "company": result.get("company_name", "Unknown"),
            "location": result.get("location", "Unknown"),
            "description": result.get("description", ""),
            "link": result.get("via", "No link")
        })

    return jobs

