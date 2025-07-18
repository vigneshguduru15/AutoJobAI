import os
import subprocess
import tempfile
import time
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
st.write("Upload your resume (PDF or DOCX), and let AI match you with top job listings!")

# --- Session state ---
if "location" not in st.session_state:
    st.session_state["location"] = "India"
if "resume_path" not in st.session_state:
    st.session_state["resume_path"] = None
if "resume_ready" not in st.session_state:
    st.session_state["resume_ready"] = False

# --- Job location selector ---
location = st.selectbox(
    "🌐 Select Job Location:",
    ["India", "United States", "United Kingdom", "Canada", "Remote"],
    index=["India", "United States", "United Kingdom", "Canada", "Remote"].index(st.session_state["location"])
)
st.session_state["location"] = location

# --- Streamlit Native File Uploader (Fixed for Mobile) ---
uploaded_file = st.file_uploader("📄 Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, uploaded_file.name)

    try:
        # Write the file in chunks (to avoid mobile upload timeout)
        with open(file_path, "wb") as f:
            while True:
                chunk = uploaded_file.read(1024 * 1024)  # 1MB per chunk
                if not chunk:
                    break
                f.write(chunk)

        # Retry to ensure file is complete
        for attempt in range(3):
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                st.session_state["resume_path"] = file_path
                st.session_state["resume_ready"] = True
                st.success(f"Resume '{uploaded_file.name}' uploaded successfully!")
                break
            time.sleep(1)
        else:
            st.error("Upload failed after multiple attempts. Please try again.")
            st.session_state["resume_ready"] = False

    except Exception as e:
        st.error(f"Upload failed: {e}")
        st.session_state["resume_ready"] = False

# --- Process the resume when ready ---
if st.session_state["resume_ready"] and st.session_state["resume_path"]:
    try:
        skills = parse_resume(st.session_state["resume_path"])
        if skills:
            st.write("🧠 **Extracted Skills:**", ", ".join(skills))
        else:
            st.warning("No valid technical skills found. Searching generic jobs.")

        # Suggest default role
        default_role = "Software Engineer"
        if "machine learning" in skills or "tensorflow" in skills:
            default_role = "Machine Learning Engineer"
        elif "react" in skills or "node.js" in skills:
            default_role = "Full Stack Developer"
        elif "aws" in skills or "mongodb" in skills:
            default_role = "Backend Developer"

        preferred_role = st.text_input("💼 Enter your preferred job role/title:", value=default_role)

        # Store jobs
        if "jobs" not in st.session_state:
            st.session_state["jobs"] = []

        # Fetch jobs
        if st.button("Find Jobs"):
            st.info(f"Searching jobs for: **{preferred_role}** in {location}")
            st.session_state["jobs"] = get_jobs(preferred_role or "Software Engineer", location=location)

        jobs = st.session_state["jobs"]

        # Display job results
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

            # Refresh button
            if st.button("🔁 Refresh Jobs"):
                st.info(f"Fetching more jobs for: **{preferred_role}** in {location}")
                st.session_state["jobs"] = get_jobs(preferred_role or "Software Engineer", location=location)

    except Exception as e:
        st.error(f"An error occurred while processing resume: {e}")
else:
    st.info("Upload your resume (PDF or DOCX) above to get started.")
