import os
import requests
import streamlit as st

def get_jobs(role="python developer", location="India", num_results=10):
    api_key = st.secrets["SERPAPI_API_KEY"]

    params = {
        "engine": "google_jobs",
        "q": role,
        "location": location,
        "api_key": api_key
    }

    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()

    results = data.get("jobs_results", [])
    jobs = []

    if not results:
        st.warning("❌ No job results found from SerpAPI.")
        return []

    for job in results[:num_results]:
        title = job.get("title", "No Title")
        description = job.get("description", "")

        # ✅ Use the first link from apply_options if available
        link = ""
        apply_options = job.get("apply_options", [])
        if apply_options and isinstance(apply_options, list):
            link = apply_options[0].get("link", "")

        if not link.startswith("http"):
            st.warning(f"⚠️ Invalid job link found for job: {title}. Skipping this job.")
            continue

        jobs.append({
            "title": title,
            "link": link,
            "description": description
        })

    return jobs
