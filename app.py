"""Module 5: Streamlit UI - AI Resume Analyzer & Job Matcher.
Run with:  python -m streamlit run app.py
"""
import streamlit as st
from src.parser import extract_text
from src.skills import extract_skills, categorize
from src.analyzer import analyze_resume
from src.matcher import load_jobs, match_jobs, match_custom_jd

st.set_page_config(page_title="AI Resume Analyzer & Job Matcher", page_icon="📄", layout="wide")
st.title("📄 AI Resume Analyzer & Job Matcher")
st.caption("Upload your resume, get an instant quality score, and see which jobs fit you best.")

uploaded = st.sidebar.file_uploader("Upload resume (PDF / DOCX / TXT)", type=["pdf", "docx", "txt"])
st.sidebar.markdown("---")
jd_input = st.sidebar.text_area("Optional: paste a job description to match against", height=200)
btn_col1, btn_col2 = st.sidebar.columns(2)
if btn_col1.button("🔍 Match JD", type="primary", use_container_width=True):
    st.session_state["jd_text"] = jd_input.strip()
    if not jd_input.strip():
        st.sidebar.warning("Please paste a job description first.")
if btn_col2.button("🗑️ Clear", use_container_width=True):
    st.session_state["jd_text"] = ""
jd_text = st.session_state.get("jd_text", "")

text = ""
if uploaded:
    try:
        text = extract_text(uploaded, uploaded.name)
    except Exception as e:
        st.error(f"Could not read file: {e}")

if not text.strip():
    st.info("👈 Upload your resume to begin.")
    st.stop()

skills = extract_skills(text)
analysis = analyze_resume(text, skills)

tab1, tab2, tab3 = st.tabs(["📊 Resume Analysis", "🎯 Job Matches", "📝 Custom JD Match"])

with tab1:
    c1, c2, c3 = st.columns(3)
    c1.metric("Resume Score", f"{analysis['score']}/100")
    c2.metric("Skills Found", len(skills))
    c3.metric("Word Count", analysis["word_count"])
    st.progress(analysis["score"] / 100)

    left, right = st.columns(2)
    with left:
        st.subheader("Sections")
        for name, ok in analysis["sections"].items():
            st.write(("✅ " if ok else "❌ ") + name)
        st.subheader("Contact Details")
        for name, ok in analysis["contact"].items():
            st.write(("✅ " if ok else "❌ ") + name)
    with right:
        st.subheader("Skills by Category")
        for cat, items in categorize(skills).items():
            st.markdown(f"**{cat}:** " + ", ".join(items))
        st.subheader("Suggestions")
        if analysis["tips"]:
            for t in analysis["tips"]:
                st.warning(t)
        else:
            st.success("Great resume! No major issues found.")

with tab2:
    results = match_jobs(text, skills, load_jobs())
    for r in results:
        with st.expander(f"{r['title']} @ {r['company']}  —  {r['score']}% match"):
            st.progress(min(r["score"], 100) / 100)
            st.markdown("**✅ Matched skills:** " + (", ".join(r["matched"]) or "None"))
            st.markdown("**⚠️ Skills to learn:** " + (", ".join(r["missing"]) or "None"))

with tab3:
    if jd_text.strip():
        r = match_custom_jd(text, skills, jd_text)
        st.metric("Match with your job description", f"{r['score']}%")
        st.progress(min(r["score"], 100) / 100)
        st.markdown("**✅ Matched skills:** " + (", ".join(r["matched"]) or "None"))
        st.markdown("**⚠️ Missing skills:** " + (", ".join(r["missing"]) or "None"))
    else:
        st.info("Paste a job description in the sidebar and click 'Match JD' to see the result.")
        """
        Junior Software Developer

We are hiring a Junior Software Developer to join our product team.

Requirements:
- Good knowledge of Python and Flask
- Experience building REST API
- Working knowledge of SQL and MySQL
- Familiar with Git and GitHub
- Understanding of OOP, data structures and algorithms
- Experience with unit testing
- Knowledge of Docker and AWS is a plus
- Familiarity with Agile methodology
- Good communication and teamwork skills
        """