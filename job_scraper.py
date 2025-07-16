import os
import streamlit as st
from serpapi import GoogleSearch

def get_jobs(role="python developer", location="India", num_results=10):
    api_key = st.secrets["SERPAPI_API_KEY"]

    params = {
        "engine": "google_jobs",
        "q": f"{role} in {location}",
        "api_key": api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    jobs = results.get("jobs_results", [])
    return jobs[:num_results]
