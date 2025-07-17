import pdfplumber
import docx
import spacy
import fitz  # PyMuPDF

nlp = spacy.load("en_core_web_sm")

def extract_text_from_resume(file):
    if file.name.endswith(".pdf"):
        try:
            text = ""
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            if not text.strip():
                doc = fitz.open(stream=file.read(), filetype="pdf")
                for page in doc:
                    text += page.get_text()
            return text
        except:
            return ""
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    return ""

def extract_skills(text):
    doc = nlp(text.lower())
    tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]
    skills_list = ["python", "java", "c++", "html", "css", "javascript", "sql", "tensorflow", "pytorch", "sklearn",
                   "pandas", "numpy", "flask", "django", "aws", "azure", "react", "node.js", "git", "linux", "docker"]
    found = list(set([token for token in tokens if token in skills_list]))
    return found
