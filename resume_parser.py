import fitz  # PyMuPDF
import io
import re

def extract_text_from_pdf(pdf_file):
    # Read from uploaded file stream
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_skills(text):
    # Simple keyword-based extraction
    keywords = [
        "python", "machine learning", "deep learning", "nlp", "sql", "aws",
        "azure", "pandas", "numpy", "data analysis", "tensorflow", "pytorch",
        "django", "flask", "react", "node", "java", "c++", "git", "docker",
        "kubernetes", "linux", "rest", "api", "html", "css", "javascript"
    ]
    found = set()
    for word in keywords:
        if re.search(rf"\b{re.escape(word)}\b", text, re.IGNORECASE):
            found.add(word)
    return list(found)
