import os
import subprocess
import tempfile
import streamlit as st
import streamlit.components.v1 as components
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
st.write("Upload your resume (PDF or DOCX) and get matched with top jobs!")

# --- Session state ---
if "location" not in st.session_state:
    st.session_state["location"] = "India"
if "resume_uploaded" not in st.session_state:
    st.session_state["resume_uploaded"] = False
if "resume_path" not in st.session_state:
    st.session_state["resume_path"] = None

# --- Location Selector ---
location = st.selectbox(
    "🌐 Select Job Location:",
    ["India", "United States", "United Kingdom", "Canada", "Remote"],
    index=["India", "United States", "United Kingdom", "Canada", "Remote"].index(st.session_state["location"])
)
st.session_state["location"] = location

# --- HTML Resume Uploader with Progress ---
st.markdown("### 📄 Upload Your Resume (PDF or DOCX)")
components.html(
    """
    <input type="file" id="resumeUploader" accept=".pdf,.docx" style="font-size:20px; padding:15px; margin:15px; border:2px solid #4CAF50; border-radius:8px;">
    <progress id="uploadProgress" value="0" max="100" style="width:100%; display:none; margin-top:10px;"></progress>
    <script>
    const uploader = document.getElementById('resumeUploader');
    const progressBar = document.getElementById('uploadProgress');
    uploader.addEventListener('change', async () => {
        const file = uploader.files[0];
        if (!file) return;
        const chunkSize = 512 * 1024; // 512 KB chunks
        let uploaded = 0;
        progressBar.style.display = 'block';
        for (let start = 0; start < file.size; start += chunkSize) {
            const chunk = file.slice(start, start + chunkSize);
            await new Promise(r => setTimeout(r, 50)); 
            uploaded += chunk.size;
            progressBar.value = Math.min(100, (uploaded / file.size) * 100);
        }
        progressBar.value = 100;
        alert("Upload completed! Click 'Analyze Resume' to process.");
    });
    </script>
    """,
    height=150
)

# --- Save uploaded file (from Streamlit uploader fallback for backend) ---
uploaded_file = st.file_uploader("Hidden Fallback (Do Not Show)", type=["pdf", "docx"], label_visibility="collapsed")

if uploaded_file and st.button("Analyze Resume"):
    temp_dir = tempfile.gettempdir()
    resume_path = os.path.join(temp_dir, uploaded_file.name)
    try:
        with open(resume_path, "wb") as f:
            f.write(uploaded_file.read())
        st.session_state["resume_uploaded"] = True
        st.session_state["resume_path"] = resume_path
        st.success(f"Resume '{uploaded_file.name}' processed successfully!")
    except Exception as e:
        st.error(f"Resume save failed: {e}")

# --- Resume Parsing and Job Fetching ---
if st.session_state["resume_uploaded"] and st.session_state["resume_path"]:
    try:
        skills = parse_resume(st.session_state["resume_path"])
        if skills:
            st.write("🧠 **Extracted Skills:**", ", ".join(skills))
        else:
            st.warning("No technical skills found. Searching general jobs.")

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
            query = preferred_role or "Software Engineer"
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
                if link != "#":
                    st.markdown(f"[**👉 Apply Here**]({link})", unsafe_allow_html=True)
                st.write("---")

            st.subheader("Top Matching Jobs")
            for job in (matched_jobs or jobs)[:10]:
                display_job(job)

            if st.button("🔁 Refresh Jobs"):
                st.info(f"Fetching more jobs for: **{preferred_role}** in {location}")
                st.session_state["jobs"] = get_jobs(query=preferred_role, location=location)

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Upload your resume using the uploader above to get started.")
