# job_scraper.py
import streamlit as st
import requests
import logging

def get_jobs(resume_skills=None, location="India", fallback=True, num_results=10):
    api_key = st.secrets["rapidapi"]["api_key"]

    url = "https://jsearch.p.rapidapi.com/search"

    # Use only top 5 skills for query
    skills_query = " ".join(resume_skills[:5]) if resume_skills else "Python Developer"

    querystring = {
        "query": f"{skills_query} jobs in {location}",
        "page": "1",
        "num_pages": "1"
    }

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    logging.warning(f"🔍 Running JSearch query: {querystring['query']}")

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        logging.error(f"❌ API Error: {response.status_code}, {response.text}")
        return []

    data = response.json()
    results = data.get("data", [])
    if not results and fallback:
        logging.warning("⚠️ No results found. Retrying with fallback query...")
        return get_jobs(resume_skills=["Software Engineer"], location=location, fallback=False)

    jobs = []
    for job in results[:num_results]:
        jobs.append({
            "title": job.get("job_title", "No Title"),
            "company": job.get("employer_name", "Unknown"),
            "location": job.get("job_city") or job.get("job_country") or "Unknown",
            "description": (job.get("job_description", "")[:300] + "..."),
            "apply_link": job.get("job_apply_link")
        })

    logging.info(f"✅ {len(jobs)} jobs fetched for {location}.")
    return jobs
