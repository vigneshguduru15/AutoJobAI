import os
import requests
import streamlit as st

def get_jobs(role="python developer", location="India", num_results=10):
    api_key = st.secrets["SERPAPI_API_KEY"]  # uses Streamlit secrets
    search_url = "https://serpapi.com/search.json"

    params = {
        "engine": "google_jobs",
        "q": f"{role} in {location}",
        "api_key": api_key,
        "hl": "en"
    }

    response = requests.get(search_url, params=params)
    data = response.json()

    job_results = data.get("jobs_results", [])[:num_results]
    valid_jobs = []

    for job in job_results:
        link = None

        # Attempt to get apply link
        if "apply_options" in job and job["apply_options"]:
            for option in job["apply_options"]:
                if "link" in option:
                    link = option["link"]
                    break

        if not link:
            st.warning("⚠️ Invalid job link found. Skipping this job.")
            continue

        valid_jobs.append({
            "title": job.get("title", "No Title"),
            "description": job.get("description", ""),
            "link": link
        })

    return valid_jobs
