import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from document.loader import pdf_to_text, docx_to_text
from graph.workflow import app_graph



# ── Page Configuration ─────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide",
)


# ── Custom Styling ─────────────────────────────────────────────────────────────

st.markdown(
    """
    <style>
    /* ── Skill Tags ─────────────────────────────────────────────────── */
    .skill-tag {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        margin: 0.2rem;
        border-radius: 2rem;
        font-size: 0.88rem;
        font-weight: 500;
    }
    .skill-default {
        background-color: #eef2f7;
        color: #2c3e50;
        border: 1px solid #d0d7e2;
    }
    .skill-match {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #a3d9a5;
    }
    .skill-missing {
        background-color: #f8d7da;
        color: #842029;
        border: 1px solid #f1aeb5;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Helper: render a list of skills as styled tags ─────────────────────────────

def _render_skill_tags(skills, css_class="skill-default"):
    """Display skills as inline styled tags. Handles list or string gracefully."""
    if isinstance(skills, list) and skills:
        tags = "".join(
            f'<span class="skill-tag {css_class}">{skill}</span>' for skill in skills
        )
        st.markdown(tags, unsafe_allow_html=True)
    elif isinstance(skills, str) and skills.strip():
        st.markdown(skills)
    else:
        st.info("None identified.")


# ── Header ─────────────────────────────────────────────────────────────────────

st.title("📄 Resume Analyzer")
st.markdown(
    "Upload your resume and paste a job description to receive a detailed "
    "skill-gap analysis, matching insights, and improvement suggestions."
)

st.divider()


# ── Input Section ──────────────────────────────────────────────────────────────

col_upload, col_jd = st.columns(2, gap="large")

with col_upload:
    st.subheader("📎 Upload Resume")
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF or DOCX)",
        type=["pdf", "docx"],
        help="Supported formats: .pdf, .docx",
    )
    if uploaded_file is not None:
        st.success(f"**{uploaded_file.name}** uploaded successfully.")

with col_jd:
    st.subheader("📋 Job Description")
    job_description = st.text_area(
        "Paste the job description below",
        height=250,
        placeholder="Paste the full job description here…",
    )

st.divider()


# ── Analyze Button ─────────────────────────────────────────────────────────────

analyze_clicked = st.button(
    "🔍 Analyze Resume", type="primary", use_container_width=True
)

if analyze_clicked:

    # ── Validation ─────────────────────────────────────────────────────────────

    if uploaded_file is None:
        st.error("⚠️ Please upload a resume file before analyzing.")
        st.stop()

    if not job_description or not job_description.strip():
        st.error("⚠️ Please provide a job description before analyzing.")
        st.stop()

    # ── Extract text from the uploaded file ────────────────────────────────────

    resume_text = ""

    try:
        file_name = uploaded_file.name.lower()

        if file_name.endswith(".pdf"):
            resume_text = pdf_to_text(uploaded_file)
        elif file_name.endswith(".docx"):
            resume_text = docx_to_text(uploaded_file)
        else:
            st.error("❌ Unsupported file type. Please upload a PDF or DOCX file.")
            st.stop()

    except Exception as e:
        st.error(f"❌ Failed to extract text from the uploaded file: {e}")
        st.stop()

    if not resume_text or not resume_text.strip():
        st.error(
            "⚠️ The uploaded file appears to be empty or could not be read. "
            "Please try a different file."
        )
        st.stop()

    # ── Invoke the existing LangGraph workflow ─────────────────────────────────

    try:
        with st.spinner(
            "Analyzing your resume against the job description… This may take a moment."
        ):
            result = app_graph.invoke(
                {
                    "resume_text": resume_text,
                    "job_description": job_description.strip(),
                }
            )

    except Exception as e:
        st.error(f"❌ An error occurred during analysis: {e}")
        st.stop()

    # ── Display Results ────────────────────────────────────────────────────────

    st.divider()
    st.header("📊 Analysis Results")

    # ── Resume Skills & Required Skills ────────────────────────────────────────

    col_resume_skills, col_required_skills = st.columns(2, gap="large")

    with col_resume_skills:
        st.subheader("📝 Resume Skills")
        _render_skill_tags(result.get("resume_skills", []), "skill-default")

    with col_required_skills:
        st.subheader("🎯 Required Skills")
        _render_skill_tags(result.get("required_skills", []), "skill-default")

    st.divider()

    # ── Matching Skills & Missing Skills ───────────────────────────────────────

    col_match, col_miss = st.columns(2, gap="large")

    with col_match:
        st.subheader("✅ Matching Skills")
        matching = result.get("matching_skills", [])
        if matching:
            _render_skill_tags(matching, "skill-match")
        else:
            st.info("No matching skills were found.")

    with col_miss:
        st.subheader("❌ Missing Skills")
        missing = result.get("missing_skills", [])
        if missing:
            _render_skill_tags(missing, "skill-missing")
        else:
            st.success("No missing skills — great match!")

    st.divider()

    # ── Suggestions ────────────────────────────────────────────────────────────

    st.subheader("💡 Suggestions")
    suggestions = result.get("suggestions", "")
    if suggestions:
        with st.expander("View Improvement Suggestions", expanded=True):
            st.markdown(suggestions)
    else:
        st.info("No suggestions were generated.")

    st.divider()

    # ── Final Report ───────────────────────────────────────────────────────────

    st.subheader("📄 Final Report")
    final_report = result.get("final_report", "")
    if final_report:
        with st.container(border=True):
            st.markdown(final_report)
    else:
        st.info("No final report was generated.")
