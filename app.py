import streamlit as st
from screening import process
from PyPDF2 import PdfReader

st.set_page_config(page_title="Resume Screening Tool", layout="wide")

st.title("Resume Screening Tool")

st.markdown("""
This tool helps evaluate candidate resumes against a given job description.

Provide the job description and upload resumes to receive a structured comparison and ranking.
""")

# ----------- FUNCTION: EXTRACT TEXT -----------

def extract_text(file):
    try:
        if file.type == "application/pdf":
            pdf = PdfReader(file)
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
            return text.strip()
        else:
            return file.read().decode("utf-8").strip()
    except:
        return ""

# ----------- JOB DESCRIPTION -----------

st.header("1. Job Description")

jd_text = st.text_area(
    "Paste the job description",
    height=200,
    placeholder="Enter role requirements, skills, experience, etc."
)

# ----------- RESUME UPLOAD -----------

st.header("2. Upload Candidate Resumes")

uploaded_files = st.file_uploader(
    "Upload resumes (PDF or TXT)",
    type=["pdf", "txt"],
    accept_multiple_files=True
)

resumes = []
names = []

if uploaded_files:
    for file in uploaded_files:
        content = extract_text(file)

        if content:
            resumes.append(content)
            names.append(file.name)
        else:
            st.warning(f"Could not extract content from {file.name}")

    st.caption(f"{len(resumes)} resume(s) ready for evaluation.")

# ----------- RUN EVALUATION -----------

st.header("3. Evaluate Candidates")

if st.button("Evaluate Candidates"):

    if not jd_text.strip():
        st.warning("Please provide the job description before proceeding.")

    elif len(resumes) == 0:
        st.warning("Please upload at least one resume.")

    else:
        with st.spinner("Analyzing resumes..."):
            df = process(jd_text, resumes, names)

        st.success("Evaluation completed successfully.")

        # ----------- RESULTS -----------

        st.subheader("Candidate Evaluation")

        st.dataframe(df)

        # ----------- TOP CANDIDATE -----------

        top_candidate = df.iloc[0]

        st.subheader("Top Candidate Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("Name")
            st.write(f"**{top_candidate['Candidate']}**")

        with col2:
            st.write("Score")
            st.write(f"**Score:** {top_candidate['Score']} (Confidence: {top_candidate['Confidence']})")

        with col3:
            st.write("Recommendation")
            st.write(f"**{top_candidate['Recommendation']}**")

        # ----------- DOWNLOAD -----------

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download results as CSV",
            data=csv,
            file_name="resume_screening_results.csv",
            mime="text/csv"
        )