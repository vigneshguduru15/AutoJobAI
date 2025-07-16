import streamlit as st
from resume_parser import extract_text_from_pdf, extract_skills
from job_scraper import get_jobs
from matcher import match_jobs

st.set_page_config(
    page_title="AutoJobAI - Resume Matcher",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("## 🤖 AutoJobAI - AI Resume Matcher")
st.markdown("Upload your Resume (PDF only)")

uploaded_file = st.file_uploader("Drag and drop file here", type=["pdf"])

# ✅ Check if resume uploaded
if uploaded_file is None:
    st.warning("⚠️ Please upload a valid PDF resume to continue.")
    st.stop()

# ✅ Extract skills from resume
resume_text = extract_text_from_pdf(uploaded_file)
user_skills = extract_skills(resume_text)

if not user_skills:
    st.error("❌ Could not extract skills from resume. Please upload a more detailed resume.")
    st.stop()

# ✅ Get job role input from user
job_role = st.text_input("Enter the job role you're looking for", value="python developer")

if job_role:
    try:
        jobs = get_jobs(role=job_role)
        if not jobs:
            st.warning("⚠️ Couldn’t find job listings. Try a different role or check your connection.")
        else:
            matched_jobs = match_jobs(user_skills, jobs)

            st.markdown("### 🎯 Top Matching Jobs:")
            for job in matched_jobs:
                st.markdown(f"**{job['title']}** — [Apply Here]({job['apply_link']}) (Match Score: `{job['match_score']:.2f}`)")
                st.markdown("---")

    except Exception as e:
        st.error(f"❌ Something went wrong: {e}")
