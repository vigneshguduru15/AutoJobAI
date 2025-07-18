# test_location_debug.py

import os
from serpapi import GoogleSearch
from dotenv import load_dotenv
import json

load_dotenv()
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

def debug_job_locations(query="Streamlit Developer", location="India"):
    params = {
        "engine": "google_jobs",
        "q": query,
        "location": location,
        "api_key": SERPAPI_API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    jobs_results = results.get("jobs_results", [])

    for idx, job in enumerate(jobs_results, 1):
        print(f"\n🔎 Job #{idx} ----------------------------")
        print(json.dumps(job, indent=2))  # Pretty print full job data

if __name__ == "__main__":
    debug_job_locations()
