# app.py

import streamlit as st
from dotenv import load_dotenv
from resume_parser import extract_skills_from_resume
from job_scraper import get_jobs
from matcher import match_jobs

load_dotenv()

st.set_page_config(page_title="AutoJobAI", layout="centered")
st.title("🤖 AutoJobAI - Smart Job Matcher")
st.markdown("Upload your resume and let AI match you with top job listings!")

# Location selector (default: India)
location = st.selectbox(
    "🌍 Select Job Location:",
    ["India", "United States", "Remote"],
    index=0
)

# Upload Resume
uploaded_file = st.file_uploader("📄 Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file is not None:
    with st.spinner("🔍 Analyzing your resume..."):
        resume_skills = extract_skills_from_resume(uploaded_file)
        st.success("✅ Resume analyzed successfully!")
        st.markdown("### 🧠 Extracted Skills:")
        st.write(", ".join(resume_skills) if resume_skills else "No skills found.")

        with st.spinner(f"🔎 Fetching jobs in {location} via RapidAPI..."):
            jobs = get_jobs(resume_skills=resume_skills, location=location)
            if not jobs:
                st.warning("⚠️ No jobs fetched. Try again later or check your API key.")
            else:
                matched_jobs = match_jobs(resume_skills, jobs)

                if matched_jobs:
                    st.markdown("## 🎯 Top Matching Jobs")
                    for job in matched_jobs:
                        st.markdown(f"**{job['title']}**")
                        st.markdown(f"📍 {job['location']}")
                        if job["apply_link"]:
                            st.markdown(f"[🔗 Apply Now]({job['apply_link']})", unsafe_allow_html=True)
                        else:
                            st.warning("⚠️ No valid apply link found.")
                        st.markdown("---")
                else:
                    st.warning("⚠️ No matched jobs found. Try uploading a different resume.")
