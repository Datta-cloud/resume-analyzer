# 📄 AI Resume Analyzer

An AI-powered Resume Analyzer that evaluates resumes like ATS (Applicant Tracking Systems) and provides actionable feedback using NLP and LLMs.

🚀 **Live App:** https://resume-checker-07.streamlit.app

---

## 🔥 Features

- 📂 Upload Resume (PDF / DOCX)
- 💼 Paste Job Description
- 📊 ATS-style Match Score
- 🛠️ Skills Matching (Matched / Missing / Extra)
- 🤖 AI Suggestions using Groq (LLM)
- 🎯 Actionable Resume Improvements

---

## 🧠 Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **NLP:** spaCy
- **AI Model:** Groq (LLaMA 3.1)
- **Libraries:** scikit-learn, PyMuPDF, python-docx

---

## ⚙️ How It Works

1. Extracts resume text from PDF/DOCX  
2. Uses NLP to identify:
   - Name  
   - Skills  
   - Education  
3. Compares with job description  
4. Calculates match score  
5. Uses LLM to generate improvement suggestions  


## 🚀 Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/Datta-cloud/resume-analyzer.git
cd resume-analyzer
2. Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
3. Install dependencies
pip install -r requirements.txt
4. Run the app
streamlit run app.py
🔑 API Setup
For local development

Create a .env file:

GROQ_API_KEY=your_api_key_here
For deployment (Streamlit Cloud)
Go to App Settings → Secrets
Add:
GROQ_API_KEY = "your_api_key_here"
⚠️ Important Notes
Do NOT upload .env file to GitHub
Keep your API keys secure
Ensure spaCy model is installed via requirements.txt
🎯 Future Improvements
📄 Resume Auto-Improvement (Rewrite)
📊 ATS Score Breakdown Chart
🌐 Multi-language support
📥 Download improved resume
📌 About

This project simulates real-world ATS systems and helps users optimize resumes for job applications using AI.

⭐ Support

If you found this project useful:

⭐ Star the repository
🔗 Share with others
💡 Suggest improvements
