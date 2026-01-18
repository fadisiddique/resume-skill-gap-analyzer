# resume-skill-gap-analyzer
End-to-end NLP system for semantic resume and job description skill matching using sentence embeddings and FastAPI.

# Resume Skill Gap Analyzer

An NLP-based system that compares a candidate’s resume with a job description to identify matched and missing skills using semantic similarity.

## What it Does
- Extracts text from PDF resumes
- Identifies skills using exact and semantic matching
- Compares resume skills with job description requirements
- Computes a resume–JD match score

## Tech Stack
- Python, FastAPI
- Sentence Transformers (MiniLM)
- HTML, CSS, JavaScript

## Run Locally
```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload
