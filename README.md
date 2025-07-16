# 🤖 AutoJobAI - Smart Job Finder

AutoJobAI is an AI-powered job-matching tool that helps users find the most relevant job listings based on their resume. Just upload your resume and enter your preferred job role — AutoJobAI does the rest by scraping Google Jobs and matching results using AI.

---

## 🚀 Features

- ✅ Upload PDF Resume
- 🤖 Extract Skills using NLP
- 🔍 Scrape Jobs from Google Jobs via SerpAPI
- 📊 AI Matching Score for Each Job
- 🔗 Clickable Job Application Links
- 💡 Built with Streamlit, Python

---

## 📦 Tech Stack

- Python 🐍
- Streamlit 📊
- PyMuPDF + scikit-learn + SerpAPI
- Resume Parser (NLP)
- GitHub + Streamlit Cloud Deployment

---

## 🧠 How It Works

1. **Upload Resume** → Extracts keywords/skills
2. **Enter Job Role** → You define your interest (e.g., `Python Developer`)
3. **AI Matches Jobs** → Finds relevant jobs via SerpAPI and ranks them
4. **Get Links to Apply** → Direct clickable job links in output

---

## 🛠️ Installation

```bash
git clone https://github.com/your-username/AutoJobAI.git
cd AutoJobAI
pip install -r requirements.txt
streamlit run app.py
