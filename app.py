from flask import Flask, request, render_template, jsonify
import os
import tempfile
from resume_parser import parse_resume
from matcher import match_jobs
from job_scraper import get_jobs

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_resume():
    try:
        file = request.files.get("resume")
        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        # Save resume to uploads folder
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Extract skills
        skills = parse_resume(file_path)
        if not skills:
            skills = ["general", "developer"]

        return jsonify({
            "message": "Resume uploaded",
            "skills": skills,
            "default_role": suggest_default_role(skills)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/find-jobs", methods=["POST"])
def find_jobs():
    try:
        data = request.json
        role = data.get("role", "Software Engineer")
        location = data.get("location", "India")
        skills = data.get("skills", [])

        # Fetch jobs and match
        jobs = get_jobs(query=role, location=location)
        matched_jobs = match_jobs(jobs, skills)

        return jsonify({"jobs": matched_jobs[:10]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def suggest_default_role(skills):
    role = "Software Engineer"
    skills_str = " ".join(skills).lower()
    if "machine learning" in skills_str or "tensorflow" in skills_str:
        role = "Machine Learning Engineer"
    elif "react" in skills_str or "node" in skills_str:
        role = "Full Stack Developer"
    elif "aws" in skills_str or "mongodb" in skills_str:
        role = "Backend Developer"
    return role

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
