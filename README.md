# AI Resume Analyzer & Job Matcher

A mini project for Software Engineering. It reads a resume (PDF/DOCX/TXT), extracts skills,
scores resume quality, and ranks job openings by how well the resume matches.

## Features
- Resume upload and text extraction (PDF, DOCX, TXT)
- Skill extraction using a keyword database
- Resume score out of 100 with improvement tips
- Job matching: 60% skill overlap + 40% TF-IDF cosine similarity
- Missing-skill report for each job
- Match against any pasted job description

## Project Structure
```
resume_analyzer/
├── app.py                 # Streamlit UI (presentation layer)
├── requirements.txt
├── data/jobs.json         # Job dataset (data layer)
├── samples/sample_resume.txt
├── src/
│   ├── parser.py          # Module 1: file -> text
│   ├── skills.py          # Module 2: skill extraction
│   ├── analyzer.py        # Module 3: scoring + suggestions
│   └── matcher.py         # Module 4: job matching (TF-IDF)
└── tests/test_core.py     # Unit tests
```

## How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
python -m unittest discover tests     # run unit tests
```

## Scoring Formula
Resume score (100) = Sections 30 + Contact 15 + Skills 25 + Action verbs 15 + Quantified results 5 + Length 10

Job match = 0.6 x (matched skills / required skills) + 0.4 x TF-IDF cosine similarity

## Architecture
3-layer: Presentation (app.py) -> Business logic (src/) -> Data (jobs.json).
Each module has a single responsibility, so it can be tested and changed independently.

## Future Scope
Add more jobs / live job API, use BERT embeddings for semantic matching,
user login and history, export report as PDF.
