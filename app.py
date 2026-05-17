# app.py
# -------
# This is the MAIN file — run this to start the app.
# It's the UI layer that connects all other files together.
#
# Run command: streamlit run app.py

import streamlit as st

from resume_parser import parse_resume
from nlp_engine    import extract_all
from matcher       import extract_skills_from_text, calculate_match, get_score_label
from ai_advisor    import get_suggestions


# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Analyzer")
st.caption("Upload your resume + paste a job description → get your match score + AI tips!")


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("ℹ️ How to Use")
    st.markdown("""
    1. Upload your resume (PDF or DOCX)
    2. Paste the job description
    3. Click **Analyze**
    4. See your match score & tips!
    """)
    st.divider()
    st.caption("Built with Streamlit + spaCy + Claude AI")


# ─── MAIN LAYOUT ─────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

# Left column: Upload resume
with col1:
    st.subheader("📂 Upload Resume")
    uploaded_file = st.file_uploader(
        "Choose your resume",
        type=["pdf", "docx"],
        help="Supported: PDF or Word (.docx)"
    )

# Right column: Job description
with col2:
    st.subheader("💼 Job Description")
    job_description = st.text_area(
        "Paste the job description here",
        height=200,
        placeholder="Example: We are looking for a Python developer with experience in ML, SQL, and Docker..."
    )


# ─── ANALYZE BUTTON ──────────────────────────────────────────────────────────────
st.divider()
analyze_btn = st.button("🔍 Analyze Resume", type="primary", use_container_width=True)


# ─── RESULTS ─────────────────────────────────────────────────────────────────────
if analyze_btn:

    # Check inputs
    if not uploaded_file:
        st.warning("Please upload your resume first!")
        st.stop()

    if not job_description.strip():
        st.warning("Please paste a job description!")
        st.stop()

    # ── Step 1: Read the resume ────────────────────────────────────────────────
    with st.spinner("Reading your resume..."):
        resume_text = parse_resume(uploaded_file)

    if not resume_text:
        st.error("Could not read the file. Please try a PDF or DOCX.")
        st.stop()

    # ── Step 2: Extract info from resume ──────────────────────────────────────
    with st.spinner("Extracting information..."):
        info = extract_all(resume_text)

    # ── Step 3: Match with job description ────────────────────────────────────
    with st.spinner("Matching with job description..."):
        job_skills  = extract_skills_from_text(job_description)
        match       = calculate_match(info["skills"], job_skills)
        label, color = get_score_label(match["score"])

    # ─────────────────────────────────────────────────────────────────────────
    # DISPLAY RESULTS
    # ─────────────────────────────────────────────────────────────────────────
    st.success("✅ Analysis Complete!")
    st.divider()

    # ── Section 1: Basic Info ─────────────────────────────────────────────────
    st.subheader("👤 Candidate Info")
    c1, c2, c3 = st.columns(3)
    c1.metric("Name",  info["name"])
    c2.metric("Email", info["email"])
    c3.metric("Phone", info["phone"])

    st.divider()

    # ── Section 2: Match Score ────────────────────────────────────────────────
    st.subheader("📊 Match Score")

    score_col, bar_col = st.columns([1, 3])
    score_col.metric("Your Score", f"{match['score']}%", label)
    bar_col.progress(int(match["score"]) / 100)

    st.divider()

    # ── Section 3: Skills Breakdown ───────────────────────────────────────────
    st.subheader("🛠️ Skills Breakdown")

    sk1, sk2, sk3 = st.columns(3)

    with sk1:
        st.markdown("**✅ Matched Skills**")
        if match["matched"]:
            for skill in match["matched"]:
                st.success(skill)
        else:
            st.info("No matches found")

    with sk2:
        st.markdown("**❌ Missing Skills**")
        if match["missing"]:
            for skill in match["missing"]:
                st.error(skill)
        else:
            st.info("Nothing missing! Great!")

    with sk3:
        st.markdown("**⭐ Bonus Skills (you have extra!)**")
        if match["extra"]:
            for skill in match["extra"][:8]:  # show top 8
                st.info(skill)
        else:
            st.info("None")

    st.divider()

    # ── Section 4: Education ──────────────────────────────────────────────────
    st.subheader("🎓 Education Detected")
    if info["education"]:
        st.write(", ".join(info["education"]))
    else:
        st.info("No education keywords detected")

    st.divider()

    # ── Section 5: AI Suggestions ─────────────────────────────────────────────
    st.subheader("🤖 AI Coach Suggestions")

    with st.spinner("Asking Claude AI for personalized tips..."):
        suggestions = get_suggestions(
            resume_text    = resume_text,
            job_description= job_description,
            missing_skills = match["missing"],
            score          = match["score"]
        )

    st.markdown(suggestions)

    st.divider()

    # ── Section 6: Raw Resume Text (hidden by default) ────────────────────────
    with st.expander("📃 View Raw Resume Text (Debug)"):
        st.text(resume_text[:3000])
