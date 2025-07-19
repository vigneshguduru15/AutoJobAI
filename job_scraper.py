# job_scraper.py
import os
import requests
import logging
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
logging.basicConfig(level=logging.INFO)

# Get API key from Streamlit Secrets (preferred) or .env
try:
    from streamlit import secrets
    RAPIDAPI_KEY = secrets["rapidapi"]["api_key"]
except Exception:
    RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

RAPIDAPI_HOST = "jsearch.p.rapidapi.com"

# Country codes mapping for API queries
COUNTRY_MAP = {
    "India": "in",
    "United States": "us",
    "United Kingdom": "gb",
    "Canada": "ca",
    "Remote": "us"
}

def get_jobs(query="Software Engineer", location="India"):
    """
    Fetch job listings from RapidAPI JSearch with random page number for variety.
    Returns a list of job dicts with title, company, description, and apply_link.
    """
    if not RAPIDAPI_KEY:
        logging.error("No RAPIDAPI_KEY found. Set it in Streamlit Secrets or .env")
        return []

    country_code = COUNTRY_MAP.get(location, "us")
    query = " ".join(query.split()[:5])  # Limit query length
    url = f"https://{RAPIDAPI_HOST}/search"

    # Randomize page to get fresh results
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
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            logging.error(f"API Error {response.status_code}: {response.text}")
            return []

        data = response.json()
        jobs = data.get("data", [])

        # Normalize job data and ensure clickable apply links
        for job in jobs:
            title = job.get("job_title", "No Title")
            company = job.get("employer_name", "Unknown")
            job["title"] = title
            job["company_name"] = company
            job["description"] = job.get("job_description", "No description available.")
            job["apply_link"] = (
                job.get("job_apply_link")
                or job.get("job_posting_url")
                or job.get("job_link")
                or f"https://www.google.com/search?q={title.replace(' ', '+')}+{company.replace(' ', '+')}+job"
            )

        logging.info(f"Fetched {len(jobs)} jobs (page {page_num}) for '{query}' in {location}")
        return jobs
    except Exception as e:
        logging.error(f"Job fetch failed: {e}")
        return []
