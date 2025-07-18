from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("SERPAPI_API_KEY")
print("API KEY:", api_key)

params = {
    "engine": "google_jobs",
    "q": "Python Developer",
    "location": "India",
    "api_key": api_key
}

search = GoogleSearch(params)
results = search.get_dict()
jobs = results.get("jobs_results", [])
print("✅ Jobs fetched:", len(jobs))
