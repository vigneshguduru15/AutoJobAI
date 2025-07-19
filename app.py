import os
import subprocess
import tempfile
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
st.write("Upload your resume (PDF or DOCX) to extract skills and get matched with jobs instantly!")

# --- Session State Defaults ---
if "location" not in st.session_state:
    st.session_state["location"] = "India"
if "resume_uploaded" not in st.session_state:
    st.session_state["resume_uploaded"] = False
if "resume_path" not in st.session_state:
    st.session_state["resume_path"] = None
if "skills" not in st.session_state:
    st.session_state["skills"] = []
if "jobs" not in st.session_state:
    st.session_state["jobs"] = []

# --- Location Selector ---
location = st.selectbox(
    "🌐 Select Job Location:",
    ["India", "United States", "United Kingdom", "Canada", "Remote"],
    index=["India", "United States", "United Kingdom", "Canada", "Remote"].index(st.session_state["location"])
)
st.session_state["location"] = location

# --- Styled Resume Upload (Streamlit uploader only, looks like HTML) ---
st.markdown("<h4 style='margin-top:20px;'>📄 Upload Your Resume (PDF or DOCX)</h4>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["pdf", "docx"])

# --- When Resume is Uploaded ---
if uploaded_file:
    try:
        # Save resume
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        st.session_state["resume_uploaded"] = True
        st.session_state["resume_path"] = file_path
        st.success(f"Resume '{uploaded_file.name}' uploaded successfully!")

        # Extract skills immediately
        skills = parse_resume(file_path)
        st.session_state["skills"] = skills
        if skills:
            st.write("🧠 **Extracted Skills:**", ", ".join(skills))
        else:
            st.warning("No valid technical skills found. Showing generic jobs.")

        # Suggest a role based on skills
        default_role = "Software Engineer"
        if "machine learning" in skills or "tensorflow" in skills:
            default_role = "Machine Learning Engineer"
        elif "react" in skills or "node.js" in skills:
            default_role = "Full Stack Developer"
        elif "aws" in skills or "mongodb" in skills:
            default_role = "Backend Developer"

        preferred_role = st.text_input("💼 Enter your preferred job role/title:", value=default_role)

        # Fetch jobs immediately after skills are ready
        if not st.session_state["jobs"]:
            st.info(f"Searching jobs for: **{preferred_role}** in {location}")
            st.session_state["jobs"] = get_jobs(query=preferred_role or "Software Engineer", location=location)

        # Show jobs
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

            # Refresh jobs
            if st.button("🔁 Refresh Jobs"):
                st.session_state["jobs"] = get_jobs(query=preferred_role or "Software Engineer", location=location)

    except Exception as e:
        st.error(f"An error occurred while processing your resume: {e}")
else:
    st.warning("Upload your resume using the uploader above to get started.")
