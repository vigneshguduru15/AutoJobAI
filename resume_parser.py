import os
import docx2txt
import fitz
import spacy
from PyPDF2 import PdfReader

# Load SpaCy
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

def extract_text(file_path):
    if file_path.lower().endswith(".pdf"):
        text = ""
        try:
            pdf = PdfReader(file_path)
            for page in pdf.pages:
                text += page.extract_text() or ""
        except:
            # Fallback to PyMuPDF
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text()
        return text
    elif file_path.lower().endswith(".docx"):
        return docx2txt.process(file_path)
    return ""

def parse_resume(file_path):
    text = extract_text(file_path)
    doc = nlp(text.lower())
    skills_list = [
        "python", "java", "c++", "sql", "aws", "azure", "docker", "kubernetes",
        "tensorflow", "pytorch", "machine learning", "deep learning", "flask",
        "django", "react", "node.js", "mongodb", "pandas", "numpy", "xgboost",
        "streamlit", "data science", "artificial intelligence", "nlp"
    ]
    found = [skill for skill in skills_list if skill in text.lower()]
    return list(set(found))
