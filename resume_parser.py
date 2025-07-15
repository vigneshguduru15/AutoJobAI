import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_skills(resume_text):
    skill_keywords = [
        "python", "java", "c++", "html", "css", "javascript", "react", "node",
        "machine learning", "deep learning", "nlp", "flask", "django", "sql",
        "mongodb", "git", "linux", "aws", "data science", "pandas", "numpy"
    ]

    resume_text = resume_text.lower()
    skills = [skill for skill in skill_keywords if skill in resume_text]
    return skills
