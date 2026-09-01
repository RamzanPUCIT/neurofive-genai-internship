import streamlit as st
from pypdf import PdfReader
from analyzer import analyze_resume

st.set_page_config(page_title="Resume Feedback Tool", page_icon="📄", layout="centered")

st.title("📄 AI Resume Feedback Tool")
st.caption("Paste your resume or upload a PDF, pick a target role, and get structured recruiter-style feedback.")

target_role = st.text_input("Target job role", placeholder="e.g. Junior AI Engineer")

uploaded = st.file_uploader("Upload resume (PDF)", type="pdf")
resume_text = st.text_area("Or paste your resume text here", height=250)

if uploaded is not None:
    reader = PdfReader(uploaded)
    resume_text = "\n".join(page.extract_text() or "" for page in reader.pages)
    st.success(f"PDF read successfully — {len(resume_text)} characters extracted.")

if st.button("Analyse Resume", type="primary"):
    if not target_role.strip():
        st.warning("Please enter a target job role.")
    elif len(resume_text.strip()) < 50:
        st.warning("Please provide a longer resume (at least 50 characters).")
    else:
        with st.spinner("Analysing with AI..."):
            try:
                result = analyze_resume(resume_text, target_role)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
                st.stop()

        score = result.get("match_score", 0)
        st.metric("Match Score", f"{score}/100")
        st.progress(score / 100)
        st.info(result.get("verdict", ""))

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("✅ Strengths")
            for s in result.get("strengths", []):
                st.write(f"- {s}")
        with col2:
            st.subheader("❌ Missing Skills")
            for m in result.get("missing_skills", []):
                st.write(f"- {m}")

        st.subheader("✍️ Improved Bullet Points")
        for b in result.get("improved_bullets", []):
            with st.expander(b.get("original", "")):
                st.write(b.get("improved", ""))

        flags = result.get("red_flags", [])
        if flags:
            st.subheader("⚠️ Red Flags")
            for f in flags:
                st.write(f"- {f}")

        with st.expander("🔍 Raw JSON output (structured output proof)"):
            st.json(result)