import streamlit as st
from pypdf import PdfReader
from google import genai


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# -----------------------------
# Gemini Client
# -----------------------------
client = genai.Client()


# -----------------------------
# Page Title
# -----------------------------
st.title("📄 AI Resume Analyzer")

st.write(
    "Upload your resume PDF and get an AI-powered analysis "
    "of your skills, strengths, weaknesses and job suitability."
)


# -----------------------------
# Resume Upload
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload your Resume PDF",
    type=["pdf"]
)


# -----------------------------
# Job Description
# -----------------------------
st.subheader("💼 Job Description")

job_description = st.text_area(
    "Paste the Job Description here",
    height=200,
    placeholder="Paste the job description for the position you want to apply for..."
)


# -----------------------------
# PDF Processing
# -----------------------------
if uploaded_file is not None:

    st.success("Resume uploaded successfully!")

    reader = PdfReader(uploaded_file)

    st.info(f"Total Pages: {len(reader.pages)}")

    resume_text = ""

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if text:
            resume_text += f"\n--- Page {page_number} ---\n"
            resume_text += text


    # -----------------------------
    # Check Extracted Text
    # -----------------------------
    if resume_text.strip():

        st.success("Resume text extracted successfully!")

        st.write(
            f"Characters extracted: {len(resume_text)}"
        )


        # -----------------------------
        # Show Resume Text
        # -----------------------------
        with st.expander("📋 View Extracted Resume Text"):

            st.text_area(
                "Resume Content",
                resume_text,
                height=400
            )


        # -----------------------------
        # Analyze Button
        # -----------------------------
        if st.button(
            "🤖 Analyze Resume",
            type="primary"
        ):

            if not job_description.strip():

                st.info(
                    "No Job Description provided. "
                    "Resume-only analysis will be performed."
                )


            with st.spinner(
                "AI is analyzing your resume..."
            ):

                prompt = f"""
You are an expert Resume Analyzer and Career Assistant.

Analyze the following resume carefully.

Provide the analysis in the following sections:

1. Resume Score

Give a score out of 100.

2. Skills Found

List the technical and professional skills found in the resume.

3. Strengths

List the major strengths of the candidate.

4. Weaknesses

List areas that can be improved.

5. Missing Skills

Suggest relevant skills that appear to be missing based on the candidate's profile.

6. Job Role Suggestions

Suggest suitable job roles based on the resume.

7. ATS Improvement Suggestions

Give practical suggestions to make the resume more ATS-friendly.

8. Job Description Match

Compare the resume with the provided job description.

Provide:

- Match Score out of 100
- Matching Skills
- Missing Skills
- Relevant Experience
- Skill Gap
- Recommendations to improve the match

If no job description is provided, skip this section.

9. Overall Summary

Give a short professional summary of the resume.

Important:

- Be factual and base the analysis only on the resume.
- Do not invent qualifications or experience.
- Clearly separate resume-based facts from suggestions.
- Use clear headings and bullet points.
- Keep the feedback practical.

Resume:

{resume_text}

Job Description:

{job_description}
"""


                # -----------------------------
                # Gemini API Request
                # -----------------------------
                try:

                    response = client.models.generate_content(
                        model="gemini-3.5-flash-lite",
                        contents=prompt
                    )

                    analysis = response.text


                    # -----------------------------
                    # Display Results
                    # -----------------------------
                    st.success(
                        "Resume analysis completed!"
                    )

                    st.subheader(
                        "🤖 AI Resume Analysis"
                    )

                    st.markdown(analysis)


                except Exception as e:

                    st.error(
                        "Unable to analyze the resume right now."
                    )

                    st.write(
                        f"Error: {e}"
                    )


    else:

        st.error(
            "No text could be extracted from this PDF. "
            "The PDF may be scanned or image-based."
        )