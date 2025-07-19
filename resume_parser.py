# resume_parser.py
import spacy
from PyPDF2 import PdfReader
from docx import Document

# Load SpaCy NLP model
nlp = spacy.load("en_core_web_sm")

TECH_KEYWORDS = [
    "python", "java", "c++", "sql", "mongodb", "aws", "linux", "docker",
    "machine learning", "deep learning", "tensorflow", "pytorch", "keras",
    "pandas", "numpy", "react", "react.js", "node.js", "javascript",
    "html", "css", "flask", "django", "streamlit", "fastapi", "xgboost",
    "data science", "aiml", "artificial intelligence", "scikit-learn"
]

def extract_text_from_pdf(file_path):
    try:
        text = ""
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text
    except:
        return ""

def extract_text_from_docx(file_path):
    try:
        doc = Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])
    except:
        return ""

def parse_resume(file_path):
    """Extract technical skills from a resume file."""
    text = ""
    if file_path.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.lower().endswith(".docx"):
        text = extract_text_from_docx(file_path)

    if not text:
        return []

    doc = nlp(text.lower())
    tokens = set([token.text for token in doc if token.is_alpha])

    skills = []
    for keyword in TECH_KEYWORDS:
        if any(k in tokens for k in keyword.lower().split()):
            skills.append(keyword)

    return list(dict.fromkeys(skills))
