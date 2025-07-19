import os
import subprocess
import tempfile
import json
import requests
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

# --- Page Setup ---
st.set_page_config(page_title="AutoJobAI", layout="centered")
st.title("🤖 AutoJobAI - Smart Job Matcher")
st.write("Upload your resume (PDF or DOCX), see your skills, type your desired role, and get matched with jobs automatically!")

# --- Initialize session state ---
if "location" not in st.session_state:
    st.session_state["location"] = "India"
if "resume_uploaded" not in st.session_state:
    st.session_state["resume_uploaded"] = False
if "resume_path" not in st.session_state:
    st.session_state["resume_path"] = None
if "skills" not in st.session_state:
    st.session_state["skills"] = []
if "preferred_role" not in st.session_state:
    st.session_state["preferred_role"] = "Software Engineer"
if "jobs" not in st.session_state:
    st.session_state["jobs"] = []

# --- Job location selector ---
location = st.selectbox(
    "🌐 Select Job Location:",
    ["India", "United States", "United Kingdom", "Canada", "Remote"],
    index=["India", "United States", "United Kingdom", "Canada", "Remote"].index(st.session_state["location"])
)
st.session_state["location"] = location

# --- HTML5 uploader ---
st.markdown(
    """
    <label for="resume-upload" style="font-size: 18px; font-weight: bold;">📄 Upload Your Resume (PDF or DOCX)</label>
    <input id="resume-upload" type="file" accept=".pdf,.docx" style="display:block;margin:15px 0;font-size:16px;">
    <div id="upload-status" style="color:green;margin-bottom:10px;"></div>
    <script>
        const fileInput = document.getElementById('resume-upload');
        const statusDiv = document.getElementById('upload-status');
        fileInput.addEventListener('change', () => {
            const file = fileInput.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = () => {
                const data = reader.result;
                window.parent.postMessage({type: 'resume-upload', name: file.name, data: data}, '*');
                statusDiv.textContent = `Uploaded: ${file.name} (${(file.size/1024).toFixed(1)} KB)`;
            };
            reader.readAsArrayBuffer(file);
        });
    </script>
    """,
    unsafe_allow_html=True
)

# --- JavaScript-to-Python bridge ---
uploaded_file = st.file_uploader("Hidden backup (used internally)", type=["pdf", "docx"], label_visibility="collapsed")
if uploaded_file:
    try:
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        st.session_state["resume_uploaded"] = True
        st.session_state["resume_path"] = file_path
    except Exception as e:
        st.error(f"Error saving resume: {e}")
        st.session_state["resume_uploaded"] = False
        st.session_state["resume_path"] = None

# --- Process resume & fetch jobs ---
if st.session_state["resume_uploaded"] and st.session_state["resume_path"]:
    try:
        # Extract skills
        st.session_state["skills"] = parse_resume(st.session_state["resume_path"])
        skills = st.session_state["skills"]

        if skills:
            st.write("🧠 **Extracted Skills:**", ", ".join(skills))
        else:
            st.warning("No valid technical skills found. Searching for generic jobs.")

        # Suggest role
        default_role = "Software Engineer"
        if "machine learning" in skills or "tensorflow" in skills:
            default_role = "Machine Learning Engineer"
        elif "react" in skills or "node.js" in skills:
            default_role = "Full Stack Developer"
        elif "aws" in skills or "mongodb" in skills:
            default_role = "Backend Developer"

        st.session_state["preferred_role"] = st.text_input(
            "💼 Type your preferred job role/title:",
            value=default_role
        )

        # Fetch jobs automatically when role changes
        if st.session_state["preferred_role"]:
            query = st.session_state["preferred_role"]
            st.info(f"Fetching jobs for: **{query}** in {location}")
            st.session_state["jobs"] = get_jobs(query=query, location=location)

        # Display results
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
                query = st.session_state["preferred_role"]
                st.session_state["jobs"] = get_jobs(query=query, location=location)

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.warning("Upload your resume using the uploader above to get started.")
