import os
import re
import json
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from extractors import extract_text_from_pdf, extract_text_from_docx, extract_text_from_image
from database import get_user_id, get_jobs, apply_for_job

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_resume_data(text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    Extract the following details from this resume and return valid JSON:
    - first_name
    - last_name
    - education (degree, institution, year if available)
    - experience (role, company, duration)
    Resume:
    {text}
    """
    response = model.generate_content(prompt)
    cleaned_text = re.sub(r"```(?:json)?", "", response.text).strip("` \n")
    try:
        return json.loads(cleaned_text)
    except:
        return {"error": "Invalid JSON", "raw": cleaned_text}

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("⚠ Please log in to access this page.")
    st.stop()

st.title("📂 Resume Extractor & Job Application")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "png", "jpg"])

if uploaded_file:
    if "pdf" in uploaded_file.type:
        resume_text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        resume_text = extract_text_from_docx(uploaded_file)
    else:
        resume_text = extract_text_from_image(uploaded_file)

    result = extract_resume_data(resume_text)

    if "error" not in result:
        st.success("✅ Resume extracted successfully!")

        first_name = st.text_input("First Name", result.get("first_name", ""))
        last_name = st.text_input("Last Name", result.get("last_name", ""))

        education = "\n".join(
            [f"{e.get('degree','')} - {e.get('institution','')} ({e.get('year','')})" for e in result.get("education", [])]
        )
        st.text_area("Education", education)

        experience = "\n".join(
            [f"{e.get('role','')} at {e.get('company','')} ({e.get('duration','')})" for e in result.get("experience", [])]
        )
        st.text_area("Experience", experience)

        st.subheader("📌 Apply for a Job")
        jobs = get_jobs()
        job_options = {f"{job['title']} at {job['company']} ({job['location']})": job['id'] for job in jobs}
        selected_job = st.selectbox("Select a Job", list(job_options.keys()))

        if st.button("Apply Now"):
            user_id = get_user_id(st.session_state["username"])
            job_id = job_options[selected_job]

            apply_for_job(user_id, job_id, first_name, last_name, education, experience)
            st.success(f"🎉 Successfully applied for {selected_job}!")
    else:
        st.error("❌ Could not parse resume.")
        st.code(result["raw"])
