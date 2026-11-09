"""Module 3: Resume Analyzer - section detection, contact info and quality score."""
import re

SECTIONS = {
    "Education": ["education", "academic"],
    "Experience": ["experience", "internship", "employment", "work history"],
    "Projects": ["projects", "project work"],
    "Skills": ["skills", "technical skills", "technologies"],
    "Certifications": ["certification", "certifications", "courses"],
    "Summary": ["summary", "objective", "profile"],
}

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"(?:\+?\d{1,3}[\s-]?)?\d{10}|\(?\d{3}\)?[\s-]\d{3}[\s-]\d{4}")
LINK_RE = re.compile(r"(linkedin\.com|github\.com)", re.IGNORECASE)
ACTION_VERBS = ["developed", "built", "designed", "implemented", "created", "led",
                "managed", "optimized", "improved", "deployed", "analyzed", "automated"]


def detect_sections(text: str) -> dict[str, bool]:
    lowered = text.lower()
    return {name: any(re.search(r"\b" + re.escape(k) + r"\b", lowered) for k in keys)
            for name, keys in SECTIONS.items()}


def contact_info(text: str) -> dict[str, bool]:
    return {"Email": bool(EMAIL_RE.search(text)),
            "Phone": bool(PHONE_RE.search(text)),
            "LinkedIn/GitHub": bool(LINK_RE.search(text))}


def analyze_resume(text: str, skills: list[str]) -> dict:
    """Score the resume out of 100 and generate improvement suggestions."""
    sections = detect_sections(text)
    contact = contact_info(text)
    words = len(text.split())
    verbs = sum(text.lower().count(v) for v in ACTION_VERBS)
    has_numbers = len(re.findall(r"\d+%|\d+\+|\$\d+", text))

    score = 0
    score += round(30 * sum(sections.values()) / len(sections))       # structure
    score += round(15 * sum(contact.values()) / len(contact))         # contact
    score += min(25, len(skills) * 2)                                 # skills
    score += min(15, verbs * 3)                                       # action verbs
    score += min(5, has_numbers * 5)                                  # quantified impact
    score += 10 if 250 <= words <= 900 else 4 if words > 100 else 0   # length

    tips = []
    for name, present in sections.items():
        if not present:
            tips.append(f"Add a '{name}' section.")
    for name, present in contact.items():
        if not present:
            tips.append(f"Add your {name}.")
    if len(skills) < 8:
        tips.append("List more relevant technical skills (aim for 8+).")
    if verbs < 4:
        tips.append("Use strong action verbs (developed, built, implemented...).")
    if has_numbers == 0:
        tips.append("Quantify achievements (e.g. 'improved speed by 30%').")
    if words < 250:
        tips.append("Resume looks too short; add more detail on projects.")
    elif words > 900:
        tips.append("Resume is too long; keep it to 1-2 pages.")

    return {"score": min(score, 100), "sections": sections, "contact": contact,
            "word_count": words, "tips": tips}
