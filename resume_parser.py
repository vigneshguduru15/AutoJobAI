import fitz  # PyMuPDF
import io
import re

def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_skills(text):
    # Basic skill extraction
    skills_keywords = [
        "python", "java", "c++", "machine learning", "deep learning", "nlp", "sql", "aws", "azure", 
        "docker", "kubernetes", "django", "flask", "react", "node", "html", "css", "javascript", "pytorch", "tensorflow"
    ]
    text_lower = text.lower()
    extracted = [skill for skill in skills_keywords if skill in text_lower]
    return list(set(extracted))
