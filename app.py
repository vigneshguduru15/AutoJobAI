import os
import subprocess
import tempfile
import time
import streamlit as st
from dotenv import load_dotenv
from resume_parser import parse_resume
from matcher import match_jobs
from job_scraper import get_jobs

# --- Streamlit config must be first ---
st.set_page_config(page_title="AutoJobAI", layout="centered")

# --- Ensure SpaCy model is available ---
try:
    import en_core_web_sm
except ImportError:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])

# --- Load environment variables ---
load_dotenv()

st.title("🤖 AutoJobAI - Smart Job Matcher")
st.write("Upload your resume (PDF or DOCX), see your skills, and get matched with jobs instantly!")

# --- Initialize session state ---
if "location" not in st.session_state:
    st.session_state["location"] = "India"
if "resume_uploaded" not in st.session_state:
    st.session_state["resume_uploaded"] = False
if "resume_path" not in st.session_state:
    st.session_state["resume_path"] = None

# --- Job location selector ---
location = st.selectbox(
    "🌐 Select Job Location:",
    ["India", "United States", "United Kingdom", "Canada", "Remote"],
    index=["India", "United States", "United Kingdom", "Canada", "Remote"].index(st.session_state["location"])
)
st.session_state["location"] = location

# --- Custom HTML uploader (mobile-friendly, single uploader) ---
st.markdown(
    """
    <style>
    .upload-button {
        background-color: #4CAF50;
        color: white;
        padding: 15px 32px;
        font-size: 18px;
        border-radius: 8px;
        cursor: pointer;
        display: inline-block;
        margin-top: 10px;
    }
    .upload-button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("📄 Upload Your Resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    try:
        # Save to a temp file (safe for mobile/Streamlit Cloud)
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        st.session_state["resume_uploaded"] = True
        st.session_state["resume_path"] = file_path
        st.success(f"Resume '{uploaded_file.name}' uploaded successfully!")

    except Exception as e:
        st.error(f"Upload failed: {e}")
        st.session_state["resume_uploaded"] = False
        st.session_state["resume_path"] = None

# --- Continue only if resume uploaded ---
if st.session_state["resume_uploaded"] and st.session_state["resume_path"]:
    try:
        # Extract skills
        skills = parse_resume(st.session_state["resume_path"])
        if skills:
            st.write("🧠 **Extracted Skills:**", ", ".join(skills))
        else:
            st.warning("No technical skills found. Searching generic jobs.")

        # Suggest default job role
        default_role = "Software Engineer"
        if "machine learning" in skills or "tensorflow" in skills:
            default_role = "Machine Learning Engineer"
        elif "react" in skills or "node.js" in skills:
            default_role = "Full Stack Developer"
        elif "aws" in skills or "mongodb" in skills:
            default_role = "Backend Developer"

        preferred_role = st.text_input("💼 Enter your preferred job role/title:", value=default_role)

        # Session for job results
        if "jobs" not in st.session_state:
            st.session_state["jobs"] = []

        # Fetch jobs
        if st.button("Find Jobs"):
            st.info(f"Searching jobs for: **{preferred_role}** in {location}")
            st.session_state["jobs"] = get_jobs(query=preferred_role, location=location)

        jobs = st.session_state["jobs"]

        # Display job listings
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
                st.session_state["jobs"] = get_jobs(query=preferred_role, location=location)

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.warning("Please upload your resume to start finding jobs.")
