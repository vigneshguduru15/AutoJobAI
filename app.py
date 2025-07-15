import streamlit as st
from resume_parser import extract_text_from_pdf, extract_skills
from job_scraper import get_jobs
from matcher import rank_jobs

st.set_page_config(page_title="AutoJobAI", layout="wide")
st.title("🤖 AutoJobAI - AI Resume Matcher")

resume_file = st.file_uploader("Upload your Resume (PDF only)", type=["pdf"])

if resume_file:
    with open("uploaded_resume.pdf", "wb") as f:
        f.write(resume_file.read())

    resume_text = extract_text_from_pdf("uploaded_resume.pdf")
    skills = extract_skills(resume_text)

    st.subheader("✅ Skills Extracted from Resume:")
    st.write(skills)

    job_role = st.text_input("Enter the job role you're looking for", value="python developer")

    if job_role:
        jobs = get_jobs(role=job_role)

        if not jobs:
            st.warning("⚠️ Couldn’t find job listings. Try a different role or check your connection.")
            jobs = [
                {"title": "AI Developer", "link": "https://example.com/job1"},
                {"title": "Python Engineer", "link": "https://example.com/job2"}
            ]

        matched = rank_jobs(resume_text, jobs)

        st.subheader("🎯 Top Matching Jobs:")
        for job, score in matched:
            st.markdown(f"**{job['title']}** — [Apply Here]({job['link']})  (Match Score: {round(score, 2)})")
else:
    st.info("👈 Please upload your resume to begin.")
