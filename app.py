import os
import tempfile
import time
import subprocess
import streamlit as st
from dotenv import load_dotenv
from resume_parser import parse_resume
from matcher import match_jobs
from job_scraper import get_jobs

# --- Ensure SpaCy model is available ---
try:
    import en_core_web_sm
except ImportError:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])

# --- Load environment variables ---
load_dotenv()

st.set_page_config(page_title="AutoJobAI", layout="centered")

st.title("🤖 AutoJobAI - Smart Job Matcher")
st.write("Upload your resume (PDF or DOCX), see your skills, and get matched with jobs instantly!")

# --- Initialize session state ---
if "location" not in st.session_state:
    st.session_state["location"] = "India"
if "resume_uploaded" not in st.session_state:
    st.session_state["resume_uploaded"] = False
if "resume_path" not in st.session_state:
    st.session_state["resume_path"] = None

# --- Job location selection ---
location = st.selectbox(
    "🌐 Select Job Location:",
    ["India", "United States", "United Kingdom", "Canada", "Remote"],
    index=["India", "United States", "United Kingdom", "Canada", "Remote"].index(st.session_state["location"])
)
st.session_state["location"] = location

# --- Mobile-friendly resume upload ---
def handle_resume_upload():
    uploaded_file = st.file_uploader("📄 Upload Your Resume (PDF or DOCX)", type=["pdf", "docx"])
    if uploaded_file:
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, uploaded_file.name)
        try:
            # Chunked write for mobile stability
            with open(file_path, "wb") as f:
                while True:
                    chunk = uploaded_file.read(1024 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                st.session_state["resume_uploaded"] = True
                st.session_state["resume_path"] = file_path
                st.success(f"Resume '{uploaded_file.name}' uploaded successfully!")
            else:
                st.error("Upload failed. Please try again.")
        except Exception as e:
            st.error(f"Upload failed: {e}")
            st.session_state["resume_uploaded"] = False
            st.session_state["resume_path"] = None

handle_resume_upload()

# --- Process resume & fetch jobs ---
if st.session_state["resume_uploaded"] and st.session_state["resume_path"]:
    try:
        skills = parse_resume(st.session_state["resume_path"])
        if skills:
            st.write("🧠 **Extracted Skills:**", ", ".join(skills))
        else:
            st.warning("No technical skills found. Searching for generic jobs.")

        # Suggest default job title
        default_role = "Software Engineer"
        if "machine learning" in skills or "tensorflow" in skills:
            default_role = "Machine Learning Engineer"
        elif "react" in skills or "node.js" in skills:
            default_role = "Full Stack Developer"
        elif "aws" in skills or "mongodb" in skills:
            default_role = "Backend Developer"

        preferred_role = st.text_input("💼 Enter your preferred job role/title:", value=default_role)

        if "jobs" not in st.session_state:
            st.session_state["jobs"] = []

        if st.button("Find Jobs"):
            st.info(f"Searching jobs for: **{preferred_role}** in {location}")
            query = preferred_role if preferred_role else "Software Engineer"
            st.session_state["jobs"] = get_jobs(query=query, location=location)

        jobs = st.session_state["jobs"]

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

            if st.button("🔁 Refresh Jobs"):
                st.info(f"Fetching more jobs for: **{preferred_role}** in {location}")
                query = preferred_role if preferred_role else "Software Engineer"
                st.session_state["jobs"] = get_jobs(query=query, location=location)

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.warning("Please upload your resume to find matching jobs.")
