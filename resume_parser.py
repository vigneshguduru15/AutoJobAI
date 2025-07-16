import fitz  # PyMuPDF
import re

def extract_text_from_pdf(uploaded_file):
    """Extracts text from a PDF file object uploaded via Streamlit."""
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text


def extract_skills(resume_text):
    """
    Extracts a basic list of common technical skills from resume text.
    You can expand this list based on your domain.
    """
    skills_list = [
        "python", "java", "c++", "sql", "javascript", "html", "css", "flask", "django",
        "react", "node.js", "pandas", "numpy", "tensorflow", "keras", "machine learning",
        "deep learning", "nlp", "opencv", "aws", "azure", "docker", "kubernetes", "git",
        "linux", "mongodb", "mysql", "rest api", "fastapi", "postman"
    ]
    
    found_skills = []
    resume_text_lower = resume_text.lower()
    for skill in skills_list:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, resume_text_lower):
            found_skills.append(skill)

    return list(set(found_skills))
