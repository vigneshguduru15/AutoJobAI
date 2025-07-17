from google_search_results import GoogleSearch

params = {
    "q": "Software Engineer",
    "location": "India",
    "engine": "google_jobs",
    "api_key": "your_serpapi_key_here"
}

search = GoogleSearch(params)
results = search.get_dict()
print(results.get("jobs_results", []))
