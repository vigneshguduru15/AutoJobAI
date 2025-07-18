import os
import streamlit as st
from dotenv import load_dotenv
from resume_parser import parse_resume
from matcher import match_jobs
from job_scraper import get_jobs

# Load environment variables
load_dotenv()

st.set_page_config(page_title="AutoJobAI", layout="centered")

st.title("🤖 AutoJobAI - Smart Job Matcher")
st.write("Upload your resume, select your preferred job role, and let AI match you with top job listings!")

# Permanent storage for resumes (works on mobile & Streamlit Cloud)
UPLOAD_DIR = os.path.join(os.getcwd(), "user_resumes")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Handle session state for location
if "location" not in st.session_state:
    st.session_state["location"] = "India"

location = st.selectbox(
    "🌐 Select Job Location:",
    ["India", "United States", "United Kingdom", "Canada", "Remote"],
    index=["India", "United States", "United Kingdom", "Canada", "Remote"].index(st.session_state["location"])
)
st.session_state["location"] = location

# File uploader (always required)
uploaded_file = st.file_uploader("📄 Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    # Save uploaded resume permanently for processing
    resume_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(resume_path, "wb") as f:
        f.write(uploaded_file.read())
    st.success(f"Resume '{uploaded_file.name}' uploaded successfully!")

    try:
        # Extract skills from resume
        skills = parse_resume(resume_path)

        if skills:
            st.write("🧠 **Extracted Skills:**", ", ".join(skills))
        else:
            st.warning("No valid technical skills found. Will search generic jobs.")

        # Suggest a default job role based on skills
        default_role = "Software Engineer"
        if "machine learning" in skills or "tensorflow" in skills:
            default_role = "Machine Learning Engineer"
        elif "react" in skills or "node.js" in skills:
            default_role = "Full Stack Developer"
        elif "aws" in skills or "mongodb" in skills:
            default_role = "Backend Developer"

        # Let user confirm or edit job role
        preferred_role = st.text_input(
            "💼 Enter your preferred job role/title:",
            value=default_role
        )

        # Store jobs so user can refresh without re-uploading
        if "jobs" not in st.session_state:
            st.session_state["jobs"] = []

        # Fetch jobs when "Find Jobs" is clicked
        if st.button("Find Jobs"):
            st.info(f"Searching jobs for: **{preferred_role}** in {location}")
            query = preferred_role if preferred_role else "Software Engineer"
            st.session_state["jobs"] = get_jobs(query=query, location=location)

        jobs = st.session_state["jobs"]

        # Display job listings if any exist
        if jobs:
            matched_jobs = match_jobs(jobs, skills)

            def display_job(job):
                title = job.get("title", "No Title")
                company = job.get("company_name", "Unknown")
                desc = job.get("description", "No description available.")
                link = job.get("apply_link") or "#"

                st.markdown(f"### {title}")
                st.write(f"**Company:** {company}")
                st.write(desc[:250] + "...")
                if link and link != "#":
                    st.markdown(f"[**👉 Apply Here**]({link})", unsafe_allow_html=True)
                st.write("---")

            st.subheader("Top Matching Jobs")
            if matched_jobs:
                for job in matched_jobs[:10]:
                    display_job(job)
            else:
                st.info("No strong matches found. Showing all jobs.")
                for job in jobs[:10]:
                    display_job(job)

            # Refresh button below results
            if st.button("🔁 Refresh Jobs"):
                st.info(f"Fetching more jobs for: **{preferred_role}** in {location}")
                query = preferred_role if preferred_role else "Software Engineer"
                st.session_state["jobs"] = get_jobs(query=query, location=location)

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.warning("Please upload your resume to find matching jobs.")
