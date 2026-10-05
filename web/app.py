import streamlit as st
from pathlib import Path
import json
from datetime import datetime


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="AI Job Seeker",
    page_icon="💼",
    layout="wide"
)


# -----------------------------
# Styling
# -----------------------------

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
}

.subtitle {
    font-size: 20px;
    color: #777;
}

.card {
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #ddd;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# Header
# -----------------------------

st.markdown(
    '<div class="main-title">🤖 AI Job Seeker</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your personal AI-powered job search and application assistant'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("AI Job Seeker")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Dashboard",
        "👤 My Profile",
        "📄 Resume",
        "🎯 Job Preferences",
        "🔎 Find Jobs",
        "📋 Applications"
    ]
)


# -----------------------------
# Dashboard
# -----------------------------

if page == "🏠 Dashboard":

    st.header("Welcome to your AI Job Seeker 🚀")

    st.write(
        "Register your details, upload your resume and tell the AI "
        "what type of job you want."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Jobs Found",
            "0"
        )

    with col2:
        st.metric(
            "Applications",
            "0"
        )

    with col3:
        st.metric(
            "High Matches",
            "0"
        )

    st.divider()

    st.subheader("How it works")

    st.write("""
    1. 👤 Create your profile
    2. 📄 Upload your resume
    3. 🎯 Select your preferred jobs
    4. 🔎 AI searches job sources
    5. 🧠 AI calculates job-match score
    6. 📝 AI prepares the application
    7. 📤 Application is submitted when supported
    8. 📊 You can track every application
    """)


# -----------------------------
# Profile
# -----------------------------

elif page == "👤 My Profile":

    st.header("👤 My Profile")

    st.subheader("Personal Information")

    name = st.text_input(
        "Full Name"
    )

    email = st.text_input(
        "Email"
    )

    phone = st.text_input(
        "Phone Number"
    )

    location = st.text_input(
        "Current Location"
    )

    st.subheader("Education")

    degree = st.text_input(
        "Degree",
        value="B.Tech"
    )

    branch = st.text_input(
        "Branch",
        value="Metallurgical and Materials Engineering"
    )

    college = st.text_input(
        "College",
        value="NIT Durgapur"
    )

    graduation_year = st.number_input(
        "Graduation Year",
        min_value=2000,
        max_value=2100,
        value=2026
    )

    cgpa = st.number_input(
        "CGPA",
        min_value=0.0,
        max_value=10.0,
        value=6.36,
        step=0.01
    )

    st.subheader("Skills")

    skills = st.text_area(
        "Your Skills",
        placeholder="Python, SQL, Excel, Power BI, XRD, SEM..."
    )

    if st.button("💾 Save Profile", type="primary"):

        profile = {
            "name": name,
            "email": email,
            "phone": phone,
            "location": location,
            "degree": degree,
            "branch": branch,
            "college": college,
            "graduation_year": graduation_year,
            "cgpa": cgpa,
            "skills": skills,
            "updated_at": datetime.now().isoformat()
        }

        st.session_state["profile"] = profile

        st.success(
            "Profile saved successfully!"
        )


# -----------------------------
# Resume
# -----------------------------

elif page == "📄 Resume":

    st.header("📄 Upload Your Resume")

    st.info(
        "Upload your latest resume. The AI will later extract "
        "education, skills, experience and projects from it."
    )

    uploaded_resume = st.file_uploader(
        "Choose your resume",
        type=["pdf", "docx"]
    )

    if uploaded_resume:

        st.success(
            f"Resume uploaded: {uploaded_resume.name}"
        )

        st.session_state["resume_name"] = uploaded_resume.name

        st.subheader("Resume Analysis")

        st.write(
            "AI resume parsing will be connected in the next stage."
        )


# -----------------------------
# Job Preferences
# -----------------------------

elif page == "🎯 Job Preferences":

    st.header("🎯 What type of job are you looking for?")

    st.subheader("Preferred Job Roles")

    roles = st.multiselect(
        "Select roles",
        [
            "Graduate Engineer Trainee",
            "GET",
            "Graduate Engineer",
            "Trainee Engineer",
            "Management Trainee",
            "Quality Engineer",
            "Production Engineer",
            "Process Engineer",
            "Metallurgy Engineer",
            "Materials Engineer",
            "Data Analyst",
            "Data Analyst Intern",
            "Business Analyst",
            "Banking Operations Analyst",
            "Software Engineer Intern"
        ]
    )

    st.subheader("Preferred Domains")

    domains = st.multiselect(
        "Select domains",
        [
            "Metallurgy",
            "Materials",
            "Steel",
            "Manufacturing",
            "Quality",
            "Production",
            "Process",
            "Data Analytics",
            "Banking",
            "IT",
            "Research"
        ]
    )

    st.subheader("Preferred Locations")

    locations = st.text_input(
        "Locations",
        placeholder="Kolkata, Delhi, Bengaluru, Hyderabad, Remote, India"
    )

    st.subheader("Experience Level")

    experience = st.multiselect(
        "Allowed experience levels",
        [
            "Fresher",
            "Graduate",
            "Internship",
            "Trainee",
            "0-1 years",
            "1-2 years"
        ]
    )

    st.subheader("Minimum Match Score")

    min_score = st.slider(
        "AI Match Score",
        0,
        100,
        60
    )

    if st.button("💾 Save Job Preferences", type="primary"):

        preferences = {
            "roles": roles,
            "domains": domains,
            "locations": locations,
            "experience": experience,
            "minimum_match_score": min_score
        }

        st.session_state["preferences"] = preferences

        st.success(
            "Job preferences saved!"
        )


# -----------------------------
# Find Jobs
# -----------------------------

elif page == "🔎 Find Jobs":

    st.header("🔎 AI Job Search")

    st.write(
        "The AI will search available job sources and rank "
        "opportunities according to your profile."
    )

    if st.button(
        "🚀 Search Jobs Now",
        type="primary"
    ):

        st.info(
            "Job-search engine will be connected here."
        )

        st.write(
            "Next stage: connect real job APIs and job sources."
        )


# -----------------------------
# Applications
# -----------------------------

elif page == "📋 Applications":

    st.header("📋 Application Tracker")

    st.info(
        "Your submitted and pending applications will appear here."
    )

    columns = [
        "Job",
        "Company",
        "Match Score",
        "Status",
        "Applied Date"
    ]

    st.dataframe(
        [],
        use_container_width=True
    )

    st.write(
        "Application tracking will be connected in the next stage."
    )


# -----------------------------
# Footer
# -----------------------------

st.divider()

st.caption(
    "AI Job Seeker — Personal Job Search & Application Assistant"
)
