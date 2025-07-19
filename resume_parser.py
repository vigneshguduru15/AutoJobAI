import os
import docx2txt
import fitz  # PyMuPDF
import spacy

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

TECH_KEYWORDS = [
    "python", "java", "c++", "javascript", "node.js", "react", "angular",
    "sql", "mongodb", "aws", "docker", "kubernetes", "machine learning",
    "deep learning", "tensorflow", "pytorch", "flask", "django", "xgboost"
]

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text()
    except Exception as e:
        print(f"PDF parse error: {e}")
    return text

def extract_text_from_docx(file_path):
    try:
        return docx2txt.process(file_path)
    except Exception as e:
        print(f"DOCX parse error: {e}")
        return ""

def parse_resume(file_path):
    text = ""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif ext == ".docx":
        text = extract_text_from_docx(file_path)

    text = text.lower()
    skills_found = [kw for kw in TECH_KEYWORDS if kw in text]

    # Also use SpaCy to extract nouns (keywords)
    doc = nlp(text)
    for token in doc:
        if token.is_alpha and not token.is_stop and token.pos_ in ["NOUN", "PROPN"]:
            if token.text not in skills_found and len(token.text) > 3:
                skills_found.append(token.text)

    return list(set(skills_found))
