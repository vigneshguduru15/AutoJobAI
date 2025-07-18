import os
import subprocess
import tempfile
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

st.set_page_config(page_title="AutoJobAI", layout="centered")

st.title("🤖 AutoJobAI - Smart Job Matcher")
st.write("Upload your resume (mobile-friendly), and let AI match you with top job listings!")

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

# --- Uploadcare Widget (Auto-fetch) ---
st.markdown("""
<div id="uploadcare-widget"></div>
<script>
(function(){
  const script = document.createElement('script');
  script.src = "https://ucarecdn.com/libs/widget/3.x/uploadcare.full.min.js";
  script.async = true;
  script.onload = () => {
    const input = document.createElement('input');
    input.type = 'hidden';
    input.setAttribute('role', 'uploadcare-uploader');
    input.setAttribute('data-public-key', 'demopublickey');  // Replace with your Uploadcare key later
    input.setAttribute('data-tabs', 'file url');
    input.setAttribute('data-multiple', 'false');
    input.setAttribute('data-clearable', 'true');
    input.onchange = function() {
      window.parent.postMessage({ fileUrl: this.value }, "*");
    };
    document.getElementById("uploadcare-widget").appendChild(input);
  };
  document.body.appendChild(script);
})();
</script>
""", unsafe_allow_html=True)

# --- Capture file URL from widget via Streamlit's on_event ---
uploaded_url = st.experimental_get_query_params().get("fileUrl", [None])[0]

# --- Automatically fetch and save uploaded file ---
if uploaded_url and not st.session_state["resume_ready"]:
    try:
        temp_dir = tempfile.gettempdir()
        file_name = os.path.basename(uploaded_url.split("?")[0]) or "resume.pdf"
        file_path = os.path.join(temp_dir, file_name)

        r = requests.get(uploaded_url, stream=True, timeout=60)
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):  # 1MB chunks
                f.write(chunk)

        st.session_state["resume_path"] = file_path
        st.session_state["resume_ready"] = True
        st.success(f"Resume '{file_name}' uploaded successfully!")

    except Exception as e:
        st.error(f"Failed to download resume: {e}")
        st.session_state["resume_ready"] = False

# --- Process the resume once it's ready ---
if st.session_state["resume_ready"] and st.session_state["resume_path"]:
    try:
        skills = parse_resume(st.session_state["resume_path"])
        if skills:
            st.write("🧠 **Extracted Skills:**", ", ".join(skills))
        else:
            st.warning("No valid technical skills found. Searching generic jobs.")

        # Suggest job role
        default_role = "Software Engineer"
        if "machine learning" in skills or "tensorflow" in skills:
            default_role = "Machine Learning Engineer"
        elif "react" in skills or "node.js" in skills:
            default_role = "Full Stack Developer"
        elif "aws" in skills or "mongodb" in skills:
            default_role = "Backend Developer"

        preferred_role = st.text_input("💼 Enter your preferred job role/title:", value=default_role)

        # Store jobs in session
        if "jobs" not in st.session_state:
            st.session_state["jobs"] = []

        # Fetch jobs
        if st.button("Find Jobs"):
            st.info(f"Searching jobs for: **{preferred_role}** in {location}")
            st.session_state["jobs"] = get_jobs(preferred_role or "Software Engineer", location=location)

        jobs = st.session_state["jobs"]

        # Display jobs
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
                st.info(f"Fetching more jobs for: **{preferred_role}** in {location}")
                st.session_state["jobs"] = get_jobs(preferred_role or "Software Engineer", location=location)

    except Exception as e:
        st.error(f"An error occurred while processing resume: {e}")
else:
    st.info("Upload your resume using the widget above to get started.")
