import streamlit as st
from resume_parser import extract_text_from_pdf
from matcher import rank_jobs
from job_scraper import get_jobs

st.set_page_config(page_title="AutoJobAI", layout="centered")

st.title("🤖 AutoJobAI – Job Matcher")
st.write("Upload your resume and enter the job role to get matched with job listings.")

uploaded_file = st.file_uploader("📄 Upload your PDF Resume", type=["pdf"])

if uploaded_file is None:
    st.warning("⚠️ Please upload a valid PDF resume to continue.")
    st.stop()

job_role = st.text_input("💼 Enter the job role you're looking for", value="Python Developer")

if job_role:
    resume_text = extract_text_from_pdf(uploaded_file)
    jobs = get_jobs(role=job_role)

    if not jobs:
        st.warning("⚠️ Couldn’t find job listings. Try a different role or check your connection.")
    else:
        matched_jobs = rank_jobs(resume_text, jobs)

        st.subheader("🎯 Top Matching Jobs:")
        for job in matched_jobs:
            if "link" in job and job["link"].startswith("http"):
                st.markdown(f"**{job['title']}** — [Apply Here]({job['link']}) (Match Score: {job['score']})")
            else:
                st.warning("⚠️ Invalid job link found. Skipping this job.")
