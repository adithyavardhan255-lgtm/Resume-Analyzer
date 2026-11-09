"""Module 2: Skill extraction using a keyword database (dictionary-based NER)."""
import re

SKILLS = {
    "Programming": ["python", "java", "c++", "c", "javascript", "typescript", "go",
                    "kotlin", "swift", "php", "ruby", "r", "sql", "bash"],
    "Web": ["html", "css", "react", "angular", "vue", "node.js", "express",
            "django", "flask", "fastapi", "spring boot", "rest api", "bootstrap"],
    "Data/AI": ["machine learning", "deep learning", "nlp", "pandas", "numpy",
                "scikit-learn", "tensorflow", "pytorch", "opencv", "data analysis",
                "data visualization", "tableau", "power bi", "statistics"],
    "Database": ["mysql", "postgresql", "mongodb", "sqlite", "redis", "oracle"],
    "DevOps/Cloud": ["git", "github", "docker", "kubernetes", "aws", "azure",
                     "gcp", "jenkins", "ci/cd", "linux"],
    "SE Practices": ["agile", "scrum", "unit testing", "uml", "oop",
                     "data structures", "algorithms", "design patterns", "jira"],
    "Soft Skills": ["communication", "teamwork", "leadership", "problem solving"],
}

ALL_SKILLS = sorted({s for group in SKILLS.values() for s in group})


def _pattern(skill: str) -> re.Pattern:
    # word-boundary match that also works for 'c++', 'node.js', 'ci/cd'
    return re.compile(r"(?<![\w+#])" + re.escape(skill) + r"(?![\w+#])", re.IGNORECASE)


def extract_skills(text: str) -> list[str]:
    """Return the sorted list of known skills found in `text`."""
    return sorted(s for s in ALL_SKILLS if _pattern(s).search(text))


def categorize(skills: list[str]) -> dict[str, list[str]]:
    out = {}
    for cat, items in SKILLS.items():
        found = [s for s in skills if s in items]
        if found:
            out[cat] = found
    return out
