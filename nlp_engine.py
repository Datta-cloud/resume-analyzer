# nlp_engine.py
# --------------
# This file does ONE job:
# Take raw resume text and pull out important information from it.
# Example: skills, email, phone number, education, experience.

import re
import spacy

# Load spaCy English model (small version)
# Run this once: python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")


# ─── SKILLS LIST ────────────────────────────────────────────────────────────────
# Add or remove skills here as needed — this is the master list we search for.

SKILLS_LIST = [
    # Programming Languages
    "python", "java", "c", "c++", "c#", "javascript", "typescript",
    "r", "scala", "kotlin", "swift", "go", "rust", "php", "ruby",

    # Web Development
    "html", "css", "react", "angular", "vue", "node.js", "express",
    "django", "flask", "fastapi", "bootstrap", "tailwind",

    # Data Science & ML
    "machine learning", "deep learning", "nlp", "computer vision",
    "data science", "data analysis", "statistics", "numpy", "pandas",
    "matplotlib", "seaborn", "scikit-learn", "tensorflow", "keras",
    "pytorch", "opencv", "huggingface",

    # Databases
    "sql", "mysql", "postgresql", "mongodb", "sqlite", "redis",
    "firebase", "oracle",

    # Cloud & DevOps
    "aws", "azure", "gcp", "google cloud", "docker", "kubernetes",
    "git", "github", "gitlab", "linux", "jenkins", "ci/cd",

    # Tools & Others
    "excel", "power bi", "tableau", "matlab", "hadoop", "spark",
    "rest api", "graphql", "microservices", "agile", "scrum",
]


# ─── EDUCATION KEYWORDS ─────────────────────────────────────────────────────────
EDUCATION_KEYWORDS = [
    "b.tech", "btech", "b.e", "be", "bachelor", "b.sc", "bsc",
    "m.tech", "mtech", "m.e", "me", "master", "m.sc", "msc", "mba",
    "phd", "ph.d", "diploma", "12th", "hsc", "ssc", "10th",
    "computer science", "information technology", "data science",
    "artificial intelligence", "electronics", "mechanical", "civil",
]


# ─── MAIN EXTRACTION FUNCTIONS ───────────────────────────────────────────────────

def extract_email(text: str) -> str:
    """Find email address in text using regex."""
    pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    match = re.search(pattern, text)
    return match.group(0) if match else "Not Found"


def extract_phone(text: str) -> str:
    """Find Indian or international phone number in text."""
    pattern = r"(\+91[\s\-]?)?[6-9]\d{9}|(\+\d{1,3}[\s\-]?)?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{4}"
    match = re.search(pattern, text)
    return match.group(0).strip() if match else "Not Found"


def extract_skills(text: str) -> list:
    """
    Search the resume text for known skills from our SKILLS_LIST.
    Returns a list of skills found.
    """
    text_lower = text.lower()
    found_skills = []

    for skill in SKILLS_LIST:
        # Use word boundary matching so "c" doesn't match inside "science"
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill.title())  # capitalize nicely

    return sorted(set(found_skills))  # remove duplicates, sort


def extract_education(text: str) -> list:
    """Find education-related lines in the resume."""
    text_lower = text.lower()
    found = []

    for keyword in EDUCATION_KEYWORDS:
        if keyword in text_lower:
            found.append(keyword.upper())

    return sorted(set(found))


def extract_name(text: str) -> str:
    """
    Try to get the person's name using spaCy NER.
    spaCy looks for PERSON entities in the text.
    Usually the name is at the top of the resume.
    """
    # Only check first 300 characters (name is always at the top)
    doc = nlp(text[:300])

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text

    # Fallback: take the very first line if spaCy didn't find a name
    first_line = text.strip().split("\n")[0]
    return first_line if len(first_line) < 40 else "Not Found"


def extract_all(text: str) -> dict:
    """
    Master function: runs all extractions and returns a clean dictionary.
    This is what app.py will call.
    """
    return {
        "name":      extract_name(text),
        "email":     extract_email(text),
        "phone":     extract_phone(text),
        "skills":    extract_skills(text),
        "education": extract_education(text),
    }
