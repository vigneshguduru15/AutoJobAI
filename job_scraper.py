import os
import random
import logging
import requests
import streamlit as st

logging.basicConfig(level=logging.INFO)

# Load RapidAPI key from Streamlit secrets
RAPIDAPI_KEY = st.secrets["rapidapi"]["api_key"]
RAPIDAPI_HOST = "jsearch.p.rapidapi.com"

# Fallback public jobs API (no auth required, fewer results)
FALLBACK_URL = "https://remotive.io/api/remote-jobs"

COUNTRY_MAP = {
    "India": "in",
    "United States": "us",
    "United Kingdom": "gb",
    "Canada": "ca",
    "Remote": "us",
}


def fetch_from_jsearch(query, location):
    """Fetch jobs using JSearch (RapidAPI)."""
    try:
        country_code = COUNTRY_MAP.get(location, "us")
        url = f"https://{RAPIDAPI_HOST}/search"
        page_num = random.randint(1, 3)  # Rotate pages for freshness

        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": RAPIDAPI_HOST,
        }
        params = {
            "query": f"{query} in {location}",
            "page": page_num,
            "num_pages": 1,
            "country": country_code,
            "language": "en",
        }

        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code != 200:
            logging.error(f"JSearch API Error {response.status_code}: {response.text}")
            return []

        data = response.json()
        return data.get("data", [])

    except Exception as e:
        logging.error(f"JSearch fetch failed: {e}")
        return []


def fetch_from_remotive(query):
    """Fetch jobs from Remotive (fallback)."""
    try:
        params = {"search": query}
        response = requests.get(FALLBACK_URL, params=params, timeout=10)
        if response.status_code != 200:
            logging.error(f"Remotive API Error {response.status_code}: {response.text}")
            return []

        data = response.json()
        jobs = data.get("jobs", [])
        # Normalize Remotive fields to match JSearch format
        for job in jobs:
            job["title"] = job.get("title", "No Title")
            job["company_name"] = job.get("company_name", job.get("company_name", "Unknown"))
            job["description"] = job.get("description", "No description available.")
            job["apply_link"] = job.get("url") or "#"
        return jobs

    except Exception as e:
        logging.error(f"Remotive fetch failed: {e}")
        return []


def get_jobs(query="Software Engineer", location="India"):
    """Fetch jobs, preferring JSearch, falling back to Remotive."""
    jobs = fetch_from_jsearch(query, location)

    # Normalize JSearch jobs
    for job in jobs:
        job["title"] = job.get("job_title", "No Title")
        job["company_name"] = job.get("employer_name", "Unknown")
        job["description"] = job.get("job_description", "No description available.")
        job["apply_link"] = (
            job.get("job_apply_link")
            or job.get("job_posting_url")
            or job.get("job_link")
            or f"https://www.google.com/search?q={job.get('job_title','').replace(' ','+')}+{job.get('employer_name','').replace(' ','+')}+job"
        )

    if not jobs:  # Fallback if JSearch fails or is empty
        logging.warning("Falling back to Remotive API...")
        jobs = fetch_from_remotive(query)

    logging.info(f"Fetched {len(jobs)} jobs for '{query}' in {location}")
    return jobs
