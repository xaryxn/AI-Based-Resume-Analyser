# Resume Screening Tool

## Overview
This project is a practical resume screening system designed to evaluate candidates against a given job description. It processes uploaded resumes, compares them with role requirements, and generates a structured evaluation to support faster and more consistent shortlisting.

The focus was on building a simple, usable system that reflects a real hiring workflow rather than a purely theoretical solution.

---

## Features
- Accepts job description via text input or file upload (PDF/TXT)  
- Supports multiple resume uploads (PDF/TXT)  
- Generates:
  - Match score (0–100)
  - Candidate ranking
  - Key strengths
  - Key gaps
  - Final recommendation
  - Confidence level  
- Provides a short explanation for the top candidate  
- Allows downloading results as a CSV file  

---

## How It Works
1. The job description and resumes are converted into text  
2. TF-IDF vectorization is applied to represent the content numerically  
3. Cosine similarity is used to measure how closely each resume matches the job description  
4. Keyword overlap is used to identify strengths and gaps  
5. Candidates are ranked and classified based on their scores  

---

## Tech Stack
- Python  
- Pandas  
- Scikit-learn (TF-IDF, Cosine Similarity)  
- Streamlit (User Interface)  
- PyPDF2 (PDF text extraction)  

---

## Project Structure

ai-resume-screening-system/
│
├── app.py
├── screening.py
├── requirements.txt
├── README.md
│
└── data/
├── sample_job_description.txt
├── sample_resumes/

## Installation & Setup

### 1. Clone the repository
```bash
git clone <your-repo-link>
cd ai-resume-screening-system

pip install -r requirements.txt

streamlit run app.py