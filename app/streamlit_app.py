import re
import streamlit as st
from pypdf import PdfReader

from job_search import search_jobs
from job_matcher import analyze_job


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Job Seeker",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# PAGE STYLE
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
        margin-top: 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# RESUME FUNCTIONS
# =========================================================

def extract_resume_text(uploaded_file):

    try:

        reader = PdfReader(uploaded_file)

        pages = []

        for page in reader.pages:

            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n".join(pages)

    except Exception as error:

        st.error(
            f"Could not read the resume: {error}"
        )

        return ""


def clean_text(text):

    text = str(text or "")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# BUILD PROFILE FROM RESUME
# =========================================================

def build_profile_from_resume(resume_text):

    text = resume_text.lower()

    profile = {

        "education": {
            "degree": "",
            "branch": "",
            "college": "",
            "graduation_year": "",
            "cgpa": ""
        },

        "preferred_roles": [
            "Graduate Engineer Trainee",
            "GET",
            "Graduate Engineer",
            "Trainee Engineer",
            "Quality Engineer",
            "Production Engineer",
            "Process Engineer",
            "Metallurgy Engineer",
            "Materials Engineer",
            "Data Analyst",
            "Data Analyst Intern",
            "Business Analyst",
            "Banking Operations Analyst"
        ],

        "preferred_domains": [],

        "skills": [],

        "experience": []
    }


    # -----------------------------------------------------
    # COMMON SKILLS
    # -----------------------------------------------------

    skills = [

        "Python",
        "SQL",
        "C",
        "C++",
        "Java",
        "JavaScript",
        "Excel",
        "Power BI",
        "Tableau",
        "Pandas",
        "NumPy",
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "Data Analysis",
        "Data Science",
        "Statistics",
        "AWS",
        "Azure",
        "GCP",
        "Git",
        "Docker",
        "Linux",
        "MySQL",
        "MongoDB",
        "XRD",
        "SEM",
        "MAUD",
        "Rietveld Refinement",
        "Metallurgy",
        "Materials Science",
        "Quality Control",
        "Quality Assurance",
        "Production",
        "Manufacturing",
        "Process Engineering"
    ]


    for skill in skills:

        if skill.lower() in text:

            profile["skills"].append(skill)


    # -----------------------------------------------------
    # DOMAIN DETECTION
    # -----------------------------------------------------

    domain_keywords = {

        "Metallurgy": [
            "metallurgy",
            "metallurgical",
            "steel",
            "alloy",
            "materials science"
        ],

        "Manufacturing": [
            "manufacturing",
            "production",
            "plant",
            "process engineering"
        ],

        "Quality": [
            "quality control",
            "quality assurance",
            "quality engineer",
            "inspection"
        ],

        "Data Analytics": [
            "data analyst",
            "data analysis",
            "power bi",
            "pandas",
            "sql"
        ],

        "IT / Software": [
            "software engineer",
            "developer",
            "python",
            "java",
            "javascript",
            "programming"
        ],

        "Banking / Finance": [
            "banking",
            "finance",
            "financial",
            "credit",
            "bank"
        ]
    }


    for domain, keywords in domain_keywords.items():

        if any(
            keyword in text
            for keyword in keywords
        ):

            profile["preferred_domains"].append(
                domain
            )


    # -----------------------------------------------------
    # DEGREE DETECTION
    # -----------------------------------------------------

    degree_patterns = [

        "b.tech",
        "btech",
        "b.e.",
        "be",
        "m.tech",
        "mtech",
        "m.e.",
        "b.sc",
        "bsc",
        "m.sc",
        "msc",
        "mba",
        "bba",
        "bca",
        "mca"
    ]

    for degree in degree_patterns:

        if degree in text:

            profile["education"]["degree"] = degree.upper()

            break


    # -----------------------------------------------------
    # RETURN PROFILE
    # -----------------------------------------------------

    return profile


# =========================================================
# HTML CLEANER
# =========================================================

def clean_html(text):

    text = str(text or "")

    text = re.sub(
        r"<[^>]+>",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">💼 AI Job Seeker</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Upload your resume and discover matching jobs'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "Upload your resume, choose your preferred location "
    "and domain, and the system will find relevant "
    "opportunities for you."
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🎯 Job Preferences")


location_options = [
    "Any Location",
    "India",
    "Remote",
    "Kolkata",
    "Delhi",
    "Mumbai",
    "Bangalore",
    "Hyderabad",
    "Chennai",
    "Pune",
    "Gurgaon",
    "Noida",
    "International"
]


domain_options = [
    "Any Domain",
    "Metallurgy / Materials",
    "Manufacturing",
    "Quality",
    "Production",
    "Process Engineering",
    "Data Analytics",
    "IT / Software",
    "Banking / Finance",
    "Research",
    "Internship",
    "Apprenticeship"
]


location = st.sidebar.selectbox(
    "📍 Preferred Location",
    location_options
)


domain = st.sidebar.selectbox(
    "🏢 Preferred Domain",
    domain_options
)


max_jobs = st.sidebar.slider(
    "📊 Number of jobs",
    min_value=5,
    max_value=50,
    value=20,
    step=5
)


st.sidebar.divider()

st.sidebar.caption(
    "Your resume is used to personalize the current search."
)


# =========================================================
# RESUME UPLOAD
# =========================================================

st.markdown(
    "## 📄 Upload Your Resume"
)

uploaded_resume = st.file_uploader(
    "Upload your PDF resume",
    type=["pdf"],
    help="Upload a PDF resume to start your personalized job search."
)


# =========================================================
# SEARCH AFTER RESUME UPLOAD
# =========================================================

if uploaded_resume:

    st.success(
        f"Resume uploaded: **{uploaded_resume.name}**"
    )


    with st.spinner(
        "🤖 Reading your resume..."
    ):

        resume_text = extract_resume_text(
            uploaded_resume
        )


    if not resume_text:

        st.error(
            "I couldn't extract text from this PDF. "
            "Please upload a text-based PDF resume."
        )

        st.stop()


    resume_text = clean_text(
        resume_text
    )


    # -----------------------------------------------------
    # CREATE USER PROFILE
    # -----------------------------------------------------

    user_profile = build_profile_from_resume(
        resume_text
    )


    # -----------------------------------------------------
    # DOMAIN FILTER
    # -----------------------------------------------------

    if domain != "Any Domain":

        domain_keywords = {

            "Metallurgy / Materials": [
                "metallurgy",
                "metallurgical",
                "materials",
                "steel",
                "alloy"
            ],

            "Manufacturing": [
                "manufacturing",
                "manufacturing engineer"
            ],

            "Quality": [
                "quality",
                "quality control",
                "quality assurance"
            ],

            "Production": [
                "production",
                "production engineer"
            ],

            "Process Engineering": [
                "process",
                "process engineer"
            ],

            "Data Analytics": [
                "data analyst",
                "data analysis",
                "analytics",
                "business analyst"
            ],

            "IT / Software": [
                "software",
                "developer",
                "programming",
                "software engineer"
            ],

            "Banking / Finance": [
                "banking",
                "finance",
                "financial",
                "bank"
            ],

            "Research": [
                "research",
                "research assistant",
                "research fellow"
            ],

            "Internship": [
                "intern",
                "internship"
            ],

            "Apprenticeship": [
                "apprentice",
                "apprenticeship"
            ]
        }

        selected_keywords = domain_keywords.get(
            domain,
            []
        )

    else:

        selected_keywords = []


    # =====================================================
    # AUTOMATIC SEARCH
    # =====================================================

    with st.spinner(
        "🔎 Searching and matching jobs..."
    ):

        jobs = search_jobs()


    if not jobs:

        st.warning(
            "No jobs were returned by the job source. "
            "Please try again later."
        )

        st.stop()


    analyzed_jobs = []


    # =====================================================
    # ANALYZE JOBS
    # =====================================================

    for job in jobs:

        try:

            # ---------------------------------------------
            # LOCATION FILTER
            # ---------------------------------------------

            job_location = str(
                job.get(
                    "location",
                    ""
                )
            ).lower()

            if location != "Any Location":

                location_key = location.lower()

                if location == "International":

                    # Keep jobs that don't clearly belong
                    # to the main Indian locations.

                    indian_terms = [
                        "india",
                        "kolkata",
                        "delhi",
                        "mumbai",
                        "bangalore",
                        "hyderabad",
                        "chennai",
                        "pune",
                        "gurgaon",
                        "noida"
                    ]

                    if any(
                        term in job_location
                        for term in indian_terms
                    ):

                        continue

                elif location == "Remote":

                    if (
                        "remote" not in job_location
                        and "remote" not in
                        str(
                            job.get(
                                "description",
                                ""
                            )
                        ).lower()
                    ):

                        continue

                elif location_key not in job_location:

                    continue


            # ---------------------------------------------
            # DOMAIN FILTER
            # ---------------------------------------------

            if selected_keywords:

                searchable = " ".join(
                    [
                        str(
                            job.get(
                                "title",
                                ""
                            )
                        ),

                        str(
                            job.get(
                                "description",
                                ""
                            )
                        ),

                        str(
                            job.get(
                                "company",
                                ""
                            )
                        )
                    ]
                ).lower()


                if not any(
                    keyword in searchable
                    for keyword in selected_keywords
                ):

                    continue


            # ---------------------------------------------
            # AI MATCHING
            # ---------------------------------------------

            result = analyze_job(
                job,
                user_profile
            )

            analyzed_jobs.append(
                result
            )


        except Exception:

            continue


    # =====================================================
    # SORT RESULTS
    # =====================================================

    analyzed_jobs.sort(
        key=lambda x: x.get(
            "match_score",
            0
        ),
        reverse=True
    )


    displayed_jobs = analyzed_jobs[
        :max_jobs
    ]


    # =====================================================
    # RESULTS SUMMARY
    # =====================================================

    st.divider()

    st.markdown(
        "## 🔎 Recommended Jobs"
    )


    col1, col2, col3 = st.columns(3)


    high_count = sum(
        1
        for job in analyzed_jobs
        if job.get("priority") == "HIGH"
    )


    medium_count = sum(
        1
        for job in analyzed_jobs
        if job.get("priority") == "MEDIUM"
    )


    with col1:

        st.metric(
            "Jobs Found",
            len(analyzed_jobs)
        )


    with col2:

        st.metric(
            "🟢 High Matches",
            high_count
        )


    with col3:

        st.metric(
            "🟡 Medium Matches",
            medium_count
        )


    st.divider()


    # =====================================================
    # JOB RESULTS
    # =====================================================

    if not displayed_jobs:

        st.warning(
            "No jobs matched your selected "
            "location and domain."
        )


    else:

        for job in displayed_jobs:

            score = job.get(
                "match_score",
                0
            )

            priority = job.get(
                "priority",
                "LOW"
            )


            if priority == "HIGH":

                badge = "🟢 HIGH"

            elif priority == "MEDIUM":

                badge = "🟡 MEDIUM"

            else:

                badge = "🔴 LOW"


            title = job.get(
                "title",
                "Unknown Job"
            )

            company = job.get(
                "company",
                "Unknown Company"
            )

            job_location = job.get(
                "location",
                "Not specified"
            )

            description = clean_html(
                job.get(
                    "description",
                    ""
                )
            )

            url = job.get(
                "url",
                ""
            )

            source = job.get(
                "source",
                "Unknown"
            )


            with st.container(
                border=True
            ):

                left, right = st.columns(
                    [4, 1]
                )


                with left:

                    st.markdown(
                        f"### 💼 {title}"
                    )

                    st.write(
                        f"**🏢 Company:** {company}"
                    )

                    st.write(
                        f"**📍 Location:** {job_location}"
                    )

                    if description:

                        st.write(
                            description[:600]
                            + (
                                "..."
                                if len(description) > 600
                                else ""
                            )
                        )


                    reasons = job.get(
                        "match_reasons",
                        []
                    )


                    if reasons:

                        with st.expander(
                            "🤖 Why this job matches"
                        ):

                            for reason in reasons:

                                st.write(
                                    f"✅ {reason}"
                                )


                with right:

                    st.metric(
                        "Match",
                        f"{score}%"
                    )

                    st.write(
                        badge
                    )


                    if url:

                        st.link_button(
                            "🚀 Apply Now",
                            url,
                            use_container_width=True
                        )


                    st.caption(
                        f"Source: {source}"
                    )


# =========================================================
# BEFORE RESUME UPLOAD
# =========================================================

else:

    st.info(
        "📄 **Upload your resume above to start "
        "your personalized job search.**"
    )

    st.markdown(
        """
        ### How it works

        **1️⃣ Upload Resume**  
        Upload your PDF resume.

        **2️⃣ Choose Preferences**  
        Select your preferred location and domain.

        **3️⃣ AI Analysis**  
        Your resume is analyzed to identify relevant skills.

        **4️⃣ Job Search**  
        Current opportunities are searched.

        **5️⃣ AI Matching**  
        Jobs are ranked according to your resume.

        **6️⃣ Apply**  
        Open the original job posting and apply.
        """
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "💼 AI Job Seeker • Personalized job discovery assistant"
)
