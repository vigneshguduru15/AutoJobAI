import streamlit as st
from resume_parser import extract_text_from_pdf, extract_skills
from matcher import match_jobs
from job_scraper import get_jobs

st.set_page_config(page_title="AutoJobAI - Job Finder", layout="centered")

st.title("🤖 AutoJobAI - Smart Job Finder")
st.write("Upload your resume and find the best matching jobs!")

# File upload
uploaded_file = st.file_uploader("📄 Upload your resume (PDF format only)", type=["pdf"])

if uploaded_file is None:
    st.warning("⚠️ Please upload a valid PDF resume to continue.")
    st.stop()

# Extract text and skills
resume_text = extract_text_from_pdf(uploaded_file)
skills = extract_skills(resume_text)

st.success("✅ Resume parsed successfully!")
st.markdown("### 🧠 Extracted Skills:")
st.write(", ".join(skills))

# Job role input
job_role = st.text_input("🎯 Enter the job role you're looking for", value="python developer")

if job_role:
    try:
        jobs = get_jobs(role=job_role)

        if not jobs:
            st.warning("⚠️ Couldn’t find job listings. Try a different role or check your connection.")
        else:
            st.markdown("## 🎯 Top Matching Jobs:")
            matched_jobs = match_jobs(resume_text, jobs)

            for job in matched_jobs:
                if not job["link"].startswith("http"):
                    st.warning("⚠️ Invalid job link found. Skipping this job.")
                    continue

                st.markdown(f"**{job['title']}** — [Apply Here]({job['link']}) (Match Score: {job['score']})")

    except Exception as e:
        st.error(f"❌ Something went wrong: {e}")
