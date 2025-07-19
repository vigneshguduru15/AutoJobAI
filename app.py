from flask import Flask, request, render_template, jsonify
import os
import tempfile
from resume_parser import parse_resume
from job_scraper import get_jobs
from matcher import match_jobs
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", skills=None, jobs=None, role="", location="India")

@app.route("/upload", methods=["POST"])
def upload_resume():
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["resume"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Save uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Parse resume to extract skills
    skills = parse_resume(file_path)

    # Suggest default role
    default_role = "Software Engineer"
    if any(s in skills for s in ["machine learning", "tensorflow", "deep learning"]):
        default_role = "Machine Learning Engineer"
    elif any(s in skills for s in ["react", "node.js", "javascript"]):
        default_role = "Full Stack Developer"
    elif any(s in skills for s in ["aws", "mongodb"]):
        default_role = "Backend Developer"

    return jsonify({"skills": skills, "suggested_role": default_role})

@app.route("/find_jobs", methods=["POST"])
def find_jobs():
    data = request.get_json()
    role = data.get("role", "Software Engineer")
    location = data.get("location", "India")
    skills = data.get("skills", [])

    # Fetch and match jobs
    jobs = get_jobs(role, location)
    matched_jobs = match_jobs(jobs, skills)

    if not matched_jobs:
        matched_jobs = jobs  # fallback if no strong matches

    return jsonify({"jobs": matched_jobs[:10]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
