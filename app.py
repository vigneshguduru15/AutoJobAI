import os
import base64
import streamlit as st
from dotenv import load_dotenv
from resume_parser import parse_resume
from matcher import match_jobs
from job_scraper import get_jobs

# Load environment variables
load_dotenv()

st.set_page_config(page_title="AutoJobAI", layout="centered")

st.title("🤖 AutoJobAI - Smart Job Matcher")
st.write("Upload your resume, confirm upload, select your job role, and let AI match you with top job listings!")

# Always use /tmp for uploads (safe for mobile + Streamlit Cloud)
UPLOAD_DIR = "/tmp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Track session state
if "location" not in st.session_state:
    st.session_state["location"] = "India"
if "resume_uploaded" not in st.session_state:
    st.session_state["resume_uploaded"] = False
if "resume_path" not in st.session_state:
    st.session_state["resume_path"] = None

# Job location
location = st.selectbox(
    "🌐 Select Job Location:",
    ["India", "United States", "United Kingdom", "Canada", "Remote"],
    index=["India", "United States", "United Kingdom", "Canada", "Remote"].index(st.session_state["location"])
)
st.session_state["location"] = location

# Upload file
uploaded_file = st.file_uploader("📄 Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

# Wait for confirmation before processing
if uploaded_file and st.button("Analyze Resume"):
    try:
        # Convert to base64 and write to /tmp (for mobile reliability)
        file_bytes = uploaded_file.read()
        encoded = base64.b64encode(file_bytes).decode()
        resume_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(resume_path, "wb") as f:
            f.write(base64.b64decode(encoded))

        st.session_state["resume_uploaded"] = True
        st.session_state["resume_path"] = resume_path
        st.success(f"Resume '{uploaded_file.name}' uploaded and saved successfully!")

    except Exception as e:
        st.error(f"Error processing resume: {e}")

# Only continue if resume confirmed
if st.session_state["resume_uploaded"] and st.session_state["resume_path"]:
    try:
        # Extract skills
        skills = parse_resume(st.session_state["resume_path"])
        if skills:
            st.write("🧠 **Extracted Skills:**", ", ".join(skills))
        else:
            st.warning("No valid technical skills found. Will search generic jobs.")

        # Suggest a default role based on skills
        default_role = "Software Engineer"
        if "machine learning" in skills or "tensorflow" in skills:
            default_role = "Machine Learning Engineer"
        elif "react" in skills or "node.js" in skills:
            default_role = "Full Stack Developer"
        elif "aws" in skills or "mongodb" in skills:
            default_role = "Backend Developer"

        preferred_role = st.text_input("💼 Enter your preferred job role/title:", value=default_role)

        # Session storage for job results
        if "jobs" not in st.session_state:
            st.session_state["jobs"] = []

        # Find jobs button
        if st.button("Find Jobs"):
            st.info(f"Searching jobs for: **{preferred_role}** in {location}")
            query = preferred_role if preferred_role else "Software Engineer"
            st.session_state["jobs"] = get_jobs(query=query, location=location)

        jobs = st.session_state["jobs"]

        # Show job results
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

            # Refresh jobs button
            if st.button("🔁 Refresh Jobs"):
                st.info(f"Fetching more jobs for: **{preferred_role}** in {location}")
                query = preferred_role if preferred_role else "Software Engineer"
                st.session_state["jobs"] = get_jobs(query=query, location=location)

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.warning("Please upload and confirm your resume before finding jobs.")
