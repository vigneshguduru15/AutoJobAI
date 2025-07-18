# AutoJobAI🤖

AutoJobAI is an **AI-powered job matcher** that helps users find the best job opportunities based on their resume.  
The tool **extracts skills from a resume, fetches live job listings using SerpAPI (Google Jobs), and matches roles dynamically**.  
It displays the **top 10 matching jobs** with clean titles, descriptions, and working apply links.

### 🚀 Live Demo
[Click here to try AutoJobAI](https://autojobai.streamlit.app) *(Deployed on Streamlit Cloud)*

---

## Features
- **Resume Parsing & Skill Extraction** – Uses SpaCy to identify technical and soft skills.
- **Live Job Fetching** – Fetches job listings via SerpAPI (Google Jobs).
- **Dynamic Job Matching** – Ranks jobs based on relevance to resume skills.
- **Top 10 Matching Jobs** – Clean display with job titles, descriptions, and **clickable apply links**.
- **Fallback & Debugging Mode** – Shows all fetched jobs when no strong matches are found.
- **Works on Desktop & Mobile** – Fully responsive via Streamlit UI.

---

## Tech Stack
- **Frontend/Backend**: [Streamlit](https://streamlit.io)
- **Programming Language**: Python 3.9+
- **Libraries**: SpaCy, SerpAPI, Pandas, NumPy, dotenv
- **Hosting**: Streamlit Cloud
- **Version Control**: Git & GitHub

---

## Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/vigneshguduru15/AutoJobAI.git
cd AutoJobAI
