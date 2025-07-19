import spacy
from PyPDF2 import PdfReader
from docx import Document

nlp = spacy.load("en_core_web_sm")

TECH_KEYWORDS = [
    "python","java","c++","sql","mongodb","aws","linux",
    "docker","machine learning","deep learning","tensorflow",
    "pytorch","keras","pandas","numpy","react","node.js",
    "javascript","html","css","flask","django","streamlit",
    "fastapi","xgboost","data science","aiml"
]

def extract_text(path):
    text = ""
    try:
        if path.lower().endswith(".pdf"):
            reader = PdfReader(path)
            for page in reader.pages:
                text += page.extract_text() or ""
        elif path.lower().endswith(".docx"):
            doc = Document(path)
            text += "\n".join(p.text for p in doc.paragraphs)
    except:
        return ""
    return text

def parse_resume(path):
    text = extract_text(path).lower()
    if not text: return []
    doc = nlp(text)
    tokens = {t.text for t in doc if t.is_alpha}
    return [k for k in TECH_KEYWORDS if any(w in tokens for w in k.lower().split())]
