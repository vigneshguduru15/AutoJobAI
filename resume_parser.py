# resume_parser.py
import docx2txt
import fitz  # PyMuPDF
import spacy

nlp = spacy.load("en_core_web_sm")

COMMON_SKILLS = {
    "python", "java", "sql", "html", "css", "javascript",
    "tensorflow", "pandas", "numpy", "flask", "streamlit",
    "scikit-learn", "xgboost", "mongodb", "git", "docker",
    "linux", "machine learning", "deep learning", "data analysis",
    "mern stack", "web development", "ai", "ml", "nlp"
}

def extract_text_from_pdf(file):
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(file):
    return docx2txt.process(file)

def extract_skills_from_resume(file):
    filename = file.name.lower()
    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(file)
    elif filename.endswith(".docx"):
        text = extract_text_from_docx(file)
    else:
        return []

    doc = nlp(text.lower())
    tokens = {token.text.strip() for token in doc if token.is_alpha and len(token.text) > 2}
    return list(tokens & COMMON_SKILLS)
