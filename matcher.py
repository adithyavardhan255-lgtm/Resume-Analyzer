"""Module 4: Job Matcher - TF-IDF cosine similarity + skill overlap."""
import json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .skills import extract_skills

JOBS_FILE = Path(__file__).resolve().parent.parent / "data" / "jobs.json"


def load_jobs(path=JOBS_FILE) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def text_similarity(resume_text: str, job_texts: list[str]) -> list[float]:
    """Cosine similarity of the resume against each job description (0-1)."""
    vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vec.fit_transform([resume_text] + job_texts)
    return cosine_similarity(matrix[0:1], matrix[1:]).flatten().tolist()


def match_jobs(resume_text: str, resume_skills: list[str], jobs: list[dict]) -> list[dict]:
    """Rank jobs. Final score = 60% skill overlap + 40% text similarity."""
    sims = text_similarity(resume_text, [j["title"] + " " + j["description"] for j in jobs])
    results = []
    for job, sim in zip(jobs, sims):
        required = set(extract_skills(job["description"])) | {s.lower() for s in job.get("skills", [])}
        have = sorted(required & set(resume_skills))
        missing = sorted(required - set(resume_skills))
        skill_score = len(have) / len(required) if required else 0
        final = round(100 * (0.6 * skill_score + 0.4 * min(sim * 2, 1)), 1)
        results.append({"title": job["title"], "company": job["company"],
                        "score": final, "matched": have, "missing": missing})
    return sorted(results, key=lambda r: r["score"], reverse=True)


def match_custom_jd(resume_text: str, resume_skills: list[str], jd_text: str) -> dict:
    """Match the resume against a pasted job description."""
    job = {"title": "Custom Job", "company": "-", "description": jd_text, "skills": []}
    return match_jobs(resume_text, resume_skills, [job])[0]
