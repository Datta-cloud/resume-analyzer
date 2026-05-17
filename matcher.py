# matcher.py
# -----------
# This file does ONE job:
# Compare the resume's skills with the job description
# and return a match score + what's missing.

import re
from nlp_engine import SKILLS_LIST


def extract_skills_from_text(text: str) -> list:
    """
    Same skill extraction logic — works for job descriptions too.
    We reuse the same SKILLS_LIST from nlp_engine.
    """
    text_lower = text.lower()
    found = []

    for skill in SKILLS_LIST:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.append(skill.title())

    return sorted(set(found))


def calculate_match(resume_skills: list, job_skills: list) -> dict:
    """
    Compare resume skills vs job required skills.

    Returns:
    - score         : percentage match (0 to 100)
    - matched       : skills present in both resume and job
    - missing       : skills in job but NOT in resume
    - extra         : skills in resume but not asked in job (bonus!)
    """
    # Convert to sets for easy comparison
    resume_set = set([s.lower() for s in resume_skills])
    job_set    = set([s.lower() for s in job_skills])

    # Skills found in both
    matched = resume_set & job_set

    # Skills job wants but resume doesn't have
    missing = job_set - resume_set

    # Skills resume has but job didn't ask for (extra value!)
    extra = resume_set - job_set

    # Score = how many job skills you have / total job skills * 100
    if len(job_set) == 0:
        score = 0
    else:
        score = round((len(matched) / len(job_set)) * 100, 1)

    return {
        "score":   score,
        "matched": sorted([s.title() for s in matched]),
        "missing": sorted([s.title() for s in missing]),
        "extra":   sorted([s.title() for s in extra]),
    }


def get_score_label(score: float) -> tuple:
    """
    Convert numeric score to a human-readable label and emoji.
    Returns (label, color) for display in Streamlit.
    """
    if score >= 80:
        return ("Excellent Match! 🔥", "green")
    elif score >= 60:
        return ("Good Match 👍", "blue")
    elif score >= 40:
        return ("Average Match ⚠️", "orange")
    else:
        return ("Weak Match ❌", "red")
