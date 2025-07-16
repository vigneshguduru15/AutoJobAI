import streamlit as st
from resume_parser import extract_text_from_pdf
from job_scraper import get_jobs
from matcher import match_jobs

st.set_page_config(page_title="AutoJobAI", layout="wide")

st.title("🤖 AutoJobAI: Smart Job Matcher")

st.markdown(
    """
    Upload your resume, and we'll automatically match you with the most relevant jobs.
    """
)

uploaded_file = st.file_uploader("📄 Upload your Resume (PDF)", type=["pdf"])

if uploaded_file is None:
    st.warning("⚠️ Please upload a valid PDF resume to continue.")
    st.stop()

# Extract resume text
try:
    resume_text = extract_text_from_pdf(uploaded_file)
except Exception as e:
    st.error(f"❌ Error reading resume: {e}")
    st.stop()

job_role = st.text_input("🔍 Enter the job role you're looking for", value="Python Developer")

if job_role:
    with st.spinner("🔎 Fetching matching jobs..."):
        try:
            jobs = get_jobs(role=job_role)

            if not jobs:
                st.warning("⚠️ Couldn’t find job listings. Try a different role or check back later.")
                st.stop()

            # Match jobs with resume
            matched_jobs = match_jobs(resume_text, jobs)

            if matched_jobs:
                st.subheader("🔍 Top Matching Jobs")

                for job in matched_jobs:
                    st.markdown(f"### {job['title']}")
                    st.markdown(f"**Score:** {job['score']}")
                    
                    # Show Apply Link
                    if job.get("link") and job["link"].startswith("http"):
                        st.markdown(f"[Apply Here]({job['link']})", unsafe_allow_html=True)
                    elif job.get("apply_options") and isinstance(job["apply_options"], list):
                        valid_links = [opt["link"] for opt in job["apply_options"] if "link" in opt and opt["link"].startswith("http")]
                        if valid_links:
                            st.markdown(f"[Apply Here]({valid_links[0]})", unsafe_allow_html=True)
                        else:
                            st.warning("⚠️ No valid application link found.")
                    else:
                        st.warning("⚠️ Invalid job link found. Skipping this job.")

            else:
                st.warning("⚠️ No relevant jobs found for your profile.")

        except Exception as e:
            st.error(f"❌ Something went wrong: {e}")
