import os
import io
import tempfile
import subprocess
import json
import streamlit as st
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
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

# --- Load Google credentials from Streamlit Secrets ---
service_account_info = json.loads(st.secrets["google"]["credentials"])
creds = service_account.Credentials.from_service_account_info(
    service_account_info,
    scopes=["https://www.googleapis.com/auth/drive"]
)
drive_service = build("drive", "v3", credentials=creds)

# --- Ensure Google Drive folder exists ---
DRIVE_FOLDER_NAME = os.getenv("DRIVE_UPLOAD_FOLDER", "AutoJobAI_Uploads")
def get_or_create_folder(folder_name):
    results = drive_service.files().list(
        q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
        fields="files(id)"
    ).execute()
    items = results.get("files", [])
    if items:
        return items[0]["id"]
    # Create folder if it doesn't exist
    file_metadata = {"name": folder_name, "mimeType": "application/vnd.google-apps.folder"}
    folder = drive_service.files().create(body=file_metadata, fields="id").execute()
    return folder.get("id")

FOLDER_ID = get_or_create_folder(DRIVE_FOLDER_NAME)

# --- Google Drive Upload/Download Functions ---
def upload_to_drive(file):
    file_name = file.name
    mime_type = "application/pdf" if file_name.endswith(".pdf") else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    file_metadata = {"name": file_name, "parents": [FOLDER_ID]}
    media = MediaIoBaseUpload(file, mimetype=mime_type)
    uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    return uploaded_file.get("id")

def download_from_drive(file_id):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    fh.seek(0)
    temp_dir = tempfile.gettempdir()
    local_path = os.path.join(temp_dir, f"resume_{file_id}.pdf")
    with open(local_path, "wb") as f:
        f.write(fh.read())
    return local_path

# --- Streamlit App ---
st.set_page_config(page_title="AutoJobAI", layout="centered")

st.title("🤖 AutoJobAI - Smart Job Matcher")
st.write("Upload your resume (PDF or DOCX), and let AI match you with top job listings (mobile & desktop friendly)!")

# Initialize session state
if "location" not in st.session_state:
    st.session_state["location"] = "India"
if "resume_uploaded" not in st.session_state:
    st.session_state["resume_uploaded"] = False
if "resume_path" not in st.session_state:
    st.session_state["resume_path"] = None

# Job location selector
location = st.selectbox(
    "🌐 Select Job Location:",
    ["India", "United States", "United Kingdom", "Canada", "Remote"],
    index=["India", "United States", "United Kingdom", "Canada", "Remote"].index(st.session_state["location"])
)
st.session_state["location"] = location

# Resume upload
uploaded_file = st.file_uploader("📄 Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
if uploaded_file:
    try:
        st.info("Uploading your resume to Google Drive... please wait")
        file_id = upload_to_drive(uploaded_file)
        resume_path = download_from_drive(file_id)
        st.session_state["resume_uploaded"] = True
        st.session_state["resume_path"] = resume_path
        st.success(f"Resume '{uploaded_file.name}' uploaded successfully!")
    except Exception as e:
        st.error(f"Upload failed: {e}")
        st.session_state["resume_uploaded"] = False
        st.session_state["resume_path"] = None

# Continue if resume uploaded
if st.session_state["resume_uploaded"] and st.session_state["resume_path"]:
    try:
        skills = parse_resume(st.session_state["resume_path"])
        if skills:
            st.write("🧠 **Extracted Skills:**", ", ".join(skills))
        else:
            st.warning("No valid technical skills found. Will search generic jobs.")

        # Suggest default job role
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
            st.session_state["jobs"] = get_jobs(query=preferred_role, location=location)

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
                st.session_state["jobs"] = get_jobs(query=preferred_role, location=location)
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.warning("Please upload your resume to find matching jobs.")
