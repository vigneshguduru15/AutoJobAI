import streamlit as st
from resume_parser import extract_text_from_resume, extract_skills
from job_scraper import get_jobs
from matcher import match_jobs

st.set_page_config(page_title="AutoJobAI", layout="centered")
st.title("🤖 AutoJobAI - Smart Job Matcher")
st.write("Upload your resume, and we’ll find jobs that match your skills automatically!")

uploaded_file = st.file_uploader("📄 Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    with st.spinner("Analyzing your resume..."):
        text = extract_text_from_resume(uploaded_file)
        skills = extract_skills(text)
        st.subheader("🧠 Extracted Skills")
        st.write(", ".join(skills))

        with st.spinner("🔍 Searching for matching jobs..."):
            query = ",".join(skills[:5]) if skills else "software engineer"
            jobs = get_jobs(query=query)

            if not jobs:
                st.warning("⚠️ No jobs fetched. Try again later or check your API key.")
            else:
                matched_jobs = match_jobs(skills, jobs)
                if matched_jobs:
                    st.subheader("🎯 Top Matching Jobs")
                    for job in matched_jobs:
                        st.markdown(f"**{job['title']}**  \n{job['company']} - {job.get('location', 'N/A')}  \n[{job['link']}]({job['link']})")
                else:
                    st.warning("No matching jobs found. Try using a resume with more relevant skills.")
