import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = "jsearch.p.rapidapi.com"

COUNTRY_MAP = {
    "India": "in",
    "United States": "us",
    "United Kingdom": "gb",
    "Canada": "ca",
    "Remote": "us"
}

def get_jobs(query="Software Engineer", location="India"):
    if not RAPIDAPI_KEY:
        logging.error("No RAPIDAPI_KEY found. Add it to your .env")
        return []

    country_code = COUNTRY_MAP.get(location, "us")
    url = f"https://{RAPIDAPI_HOST}/search"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    params = {
        "query": f"{query} in {location}",
        "page": 1,
        "num_pages": 1,
        "country": country_code
    }

    try:
        resp = requests.get(url, headers=headers, params=params)
        if resp.status_code != 200:
            logging.error(f"API Error {resp.status_code}: {resp.text}")
            return []
        data = resp.json().get("data", [])
        for job in data:
            job["title"] = job.get("job_title", "No Title")
            job["company_name"] = job.get("employer_name", "Unknown")
            job["description"] = job.get("job_description", "No description.")
            job["apply_link"] = job.get("job_apply_link") or job.get("job_posting_url") or "#"
        return data
    except Exception as e:
        logging.error(f"Job fetch failed: {e}")
        return []
