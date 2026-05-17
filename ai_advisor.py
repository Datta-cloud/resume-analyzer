# ai_advisor.py
# ---------------
# This file sends resume + job description to AI (Groq)
# and returns smart suggestions.

import os
from dotenv import load_dotenv
from groq import Groq

# Load API key from .env file
load_dotenv()


def get_suggestions(
    resume_text: str,
    job_description: str,
    missing_skills: list,
    score: float
) -> str:

    # ✅ Get API key
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return "⚠️ Please add your GROQ API key in the .env file."

    # ✅ Create Groq client
    client = Groq(api_key=api_key)

    # ✅ Build prompt
    prompt = f"""
You are an expert ATS resume reviewer and career coach.

Analyze the resume strictly based on the job description.

RETURN OUTPUT IN THIS EXACT FORMAT (no extra text):

🔴 TOP 5 CRITICAL IMPROVEMENTS:
- [Very specific fix 1]
- [Very specific fix 2]
- [Very specific fix 3]
- [Very specific fix 4]
- [Very specific fix 5]

🟡 MISSING SKILLS (MOST IMPORTANT FIRST):
- [Skill 1]
- [Skill 2]
- [Skill 3]

🟢 QUICK WINS (EASY IMPROVEMENTS):
- [1 line actionable fix]
- [1 line actionable fix]
- [1 line actionable fix]

⚡ ATS SCORE BOOST TIPS:
- [1 strong tip]
- [1 strong tip]

RULES:
- Be direct, no explanations
- No generic advice
- Focus on THIS job only
- Use short bullet points (max 12 words each)
- Prioritize impact

DATA:

MATCH SCORE: {score}%
MISSING SKILLS: {', '.join(missing_skills) if missing_skills else 'None'}

RESUME:
{resume_text[:2000]}

JOB DESCRIPTION:
{job_description[:1000]}
"""

    # ✅ Groq API call (correct format)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    # ✅ Return output
    return response.choices[0].message.content