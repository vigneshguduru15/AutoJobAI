import os
import requests
import logging
import random
from dotenv import load_dotenv
import streamlit as st

# Load API key from Streamlit secrets (fallback to .env)
load_dotenv()
logging.basicConfig(level=logging.INFO)

RAPIDAPI_KEY = st.secrets.get("rapidapi", {}).get("api_key", os.getenv("RAPIDAPI_KEY"))
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "jsearch.p.rapidapi.com")

COUNTRY_MAP = {
    "India": "in",
    "United States": "us",
    "United Kingdom": "gb",
    "Canada": "ca",
    "Remote": "us"
}

def get_jobs(query="Software Engineer", location="India"):
    """Fetch job listings from RapidAPI (JSearch) with random page for variety."""
    if not RAPIDAPI_KEY:
        logging.error("No RapidAPI key found. Set it in Streamlit Secrets or .env")
        return []

    country_code = COUNTRY_MAP.get(location, "us")
    url = f"https://{RAPIDAPI_HOST}/search"
    page_num = random.randint(1, 3)

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    params = {
        "query": f"{query} in {location}",
        "num_pages": 1,
        "page": page_num,
        "country": country_code,
        "language": "en"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        if response.status_code != 200:
            logging.error(f"API Error {response.status_code}: {response.text}")
            return []

        data = response.json()
        jobs = data.get("data", [])

        for job in jobs:
            job["title"] = job.get("job_title", "No Title")
            job["company_name"] = job.get("employer_name", "Unknown")
            job["description"] = job.get("job_description", "No description available.")
            job["apply_link"] = (
                job.get("job_apply_link")
                or job.get("job_posting_url")
                or job.get("job_link")
                or f"https://www.google.com/search?q={job.get('job_title','').replace(' ', '+')}+{job.get('employer_name','').replace(' ', '+')}+job"
            )

        logging.info(f"Fetched {len(jobs)} jobs (page {page_num}) for '{query}' in {location}")
        return jobs
    except Exception as e:
        logging.error(f"Job fetch failed: {e}")
        return []
