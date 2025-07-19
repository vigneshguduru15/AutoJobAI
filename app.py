import os
import tempfile
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

# --- Load env variables ---
load_dotenv()

# --- Page Config ---
st.set_page_config(page_title="AutoJobAI", layout="centered")
st.title("🤖 AutoJobAI - Smart Job Matcher")
st.write("Upload your resume (PDF or DOCX) to extract skills and get matched with jobs instantly!")

# --- Session defaults ---
if "resume_uploaded" not in st.session_state:
    st.session_state["resume_uploaded"] = False
if "resume_path" not in st.session_state:
    st.session_state["resume_path"] = None
if "location" not in st.session_state:
    st.session_state["location"] = "India"
if "skills" not in st.session_state:
    st.session_state["skills"] = []
if "jobs" not in st.session_state:
    st.session_state["jobs"] = []

# --- Location selector ---
location = st.selectbox(
    "🌐 Select Job Location:",
    ["India", "United States", "United Kingdom", "Canada", "Remote"],
    index=["India", "United States", "United Kingdom", "Canada", "Remote"].index(st.session_state["location"])
)
st.session_state["location"] = location

# --- Styled Resume Uploader ---
uploaded_file = st.file_uploader(
    "📄 Upload Your Resume (PDF or DOCX)",
    type=["pdf", "docx"],
    help="Drag and drop your file here or click to browse.",
    label_visibility="collapsed"
)

if uploaded_file:
    temp_dir = tempfile.gettempdir()
    resume_path = os.path.join(temp_dir, uploaded_file.name)
    with open(resume_path, "wb") as f:
        f.write(uploaded_file.read())

    st.session_state["resume_uploaded"] = True
    st.session_state["resume_path"] = resume_path

# --- Process resume automatically ---
if st.session_state["resume_uploaded"] and st.session_state["resume_path"]:
    skills = parse_resume(st.session_state["resume_path"])
    st.session_state["skills"] = skills

    if skills:
        st.write("🧠 **Extracted Skills:**", ", ".join(skills))
    else:
        st.warning("No technical skills found, showing generic jobs.")

    # Suggest job role
    default_role = "Software Engineer"
    if "machine learning" in skills or "tensorflow" in skills:
        default_role = "Machine Learning Engineer"
    elif "react" in skills or "node.js" in skills:
        default_role = "Full Stack Developer"
    elif "aws" in skills or "mongodb" in skills:
        default_role = "Backend Developer"

    role = st.text_input("💼 Enter your preferred job role/title:", value=default_role)

    # Fetch jobs automatically after upload
    if not st.session_state["jobs"]:
        st.info(f"Fetching jobs for: **{role}** in {location}...")
        st.session_state["jobs"] = get_jobs(query=role or "Software Engineer", location=location)

    jobs = st.session_state["jobs"]
    matched_jobs = match_jobs(jobs, skills)

    # --- Display Results ---
    def display_job(job):
        title = job.get("title", "No Title")
        company = job.get("company_name", "Unknown")
        desc = job.get("description", "No description")
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
        st.info(f"Refreshing jobs for: **{role}** in {location}...")
        st.session_state["jobs"] = get_jobs(query=role or "Software Engineer", location=location)

else:
    st.warning("Upload your resume to start matching jobs.")
