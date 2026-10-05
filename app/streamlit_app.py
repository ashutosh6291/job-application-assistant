import re
import streamlit as st

from job_search import search_jobs
from job_matcher import analyze_job
from profile import PROFILE


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Job Seeker",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------------
# CUSTOM STYLING
# ---------------------------------------------------------

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

    .job-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #ddd;
        margin-bottom: 15px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def clean_html(text):
    """Remove HTML tags from job descriptions."""
    if not text:
        return ""

    text = re.sub(r"<[^>]+>", " ", str(text))
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def get_priority_badge(priority):
    if priority == "HIGH":
        return "🟢 HIGH"

    if priority == "MEDIUM":
        return "🟡 MEDIUM"

    return "🔴 LOW"


def get_score_label(score):
    if score >= 80:
        return "Excellent Match"
    elif score >= 60:
        return "Good Match"
    elif score >= 40:
        return "Potential Match"

    return "Low Match"


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">💼 AI Job Seeker</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered job discovery and career assistant'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "Find relevant opportunities across Graduate Engineer, "
    "Metallurgy, Materials, Quality, Production, Process, "
    "Data Analytics and Banking roles."
)

st.divider()


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.title("🎯 Job Preferences")

st.sidebar.markdown("### Job Filters")

show_high_only = st.sidebar.checkbox(
    "🟢 HIGH priority only",
    value=False
)

location_filter = st.sidebar.text_input(
    "📍 Location",
    placeholder="Example: India, Kolkata, Remote"
)

keyword_filter = st.sidebar.text_input(
    "🔎 Keyword",
    placeholder="Example: Metallurgy, Python, Analyst"
)

max_jobs = st.sidebar.slider(
    "📊 Number of jobs",
    min_value=5,
    max_value=50,
    value=20,
    step=5
)

st.sidebar.divider()

st.sidebar.markdown("### 🎯 Target Roles")

st.sidebar.write(
    """
    • GET / Graduate Engineer  
    • Trainee Engineer  
    • Metallurgy / Materials  
    • Quality / Production  
    • Process Engineering  
    • Data Analyst  
    • Banking Operations
    """
)

st.sidebar.divider()

st.sidebar.caption(
    "AI Job Seeker v1.0"
)


# ---------------------------------------------------------
# PROFILE
# ---------------------------------------------------------

with st.expander("👤 My Profile", expanded=False):

    st.markdown("### 🎓 Education")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Degree",
            PROFILE["education"]["degree"]
        )

    with col2:
        st.metric(
            "Branch",
            "Metallurgy & Materials"
        )

    with col3:
        st.metric(
            "Graduation",
            PROFILE["education"]["graduation_year"]
        )

    with col4:
        st.metric(
            "CGPA",
            PROFILE["education"]["cgpa"]
        )

    st.markdown("### 💼 Preferred Roles")

    roles = PROFILE.get("preferred_roles", [])

    if roles:
        st.write(" • ".join(roles))

    st.markdown("### 🛠️ Skills")

    skills = PROFILE.get("skills", [])

    if skills:
        st.write(" • ".join(skills))


# ---------------------------------------------------------
# SEARCH
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">🔎 Find Your Next Opportunity</div>',
    unsafe_allow_html=True
)

st.write(
    "Search current job opportunities and see how well "
    "they match your profile."
)


search_clicked = st.button(
    "🚀 Search Jobs",
    type="primary",
    use_container_width=True
)


# ---------------------------------------------------------
# JOB SEARCH
# ---------------------------------------------------------

if search_clicked:

    with st.spinner(
        "🔎 Searching and analyzing jobs..."
    ):

        jobs = search_jobs()

    if not jobs:

        st.error(
            "No jobs were returned by the job source. "
            "Please try again later."
        )

    else:

        analyzed_jobs = []

        # ---------------------------------------------
        # ANALYZE JOBS
        # ---------------------------------------------

        for job in jobs:

            try:

                result = analyze_job(
                    job,
                    PROFILE
                )

                analyzed_jobs.append(result)

            except Exception:
                continue


        # ---------------------------------------------
        # FILTER JOBS
        # ---------------------------------------------

        if show_high_only:

            analyzed_jobs = [
                job
                for job in analyzed_jobs
                if job.get("priority") == "HIGH"
            ]


        if location_filter:

            location_text = location_filter.lower()

            analyzed_jobs = [
                job
                for job in analyzed_jobs
                if location_text in (
                    str(job.get("location", "")).lower()
                )
            ]


        if keyword_filter:

            keyword = keyword_filter.lower()

            filtered_jobs = []

            for job in analyzed_jobs:

                searchable_text = " ".join(
                    [
                        str(job.get("title", "")),
                        str(job.get("company", "")),
                        str(job.get("description", "")),
                        str(job.get("location", "")),
                    ]
                ).lower()

                if keyword in searchable_text:
                    filtered_jobs.append(job)

            analyzed_jobs = filtered_jobs


        # ---------------------------------------------
        # SORT
        # ---------------------------------------------

        analyzed_jobs.sort(
            key=lambda x: x.get(
                "match_score",
                0
            ),
            reverse=True
        )


        # ---------------------------------------------
        # LIMIT
        # ---------------------------------------------

        displayed_jobs = analyzed_jobs[:max_jobs]


        # ---------------------------------------------
        # SUMMARY
        # ---------------------------------------------

        st.success(
            f"Found {len(jobs)} jobs • "
            f"Showing {len(displayed_jobs)} matches"
        )

        # Statistics

        col1, col2, col3, col4 = st.columns(4)

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

        low_count = sum(
            1
            for job in analyzed_jobs
            if job.get("priority") == "LOW"
        )

        with col1:
            st.metric(
                "Jobs Found",
                len(jobs)
            )

        with col2:
            st.metric(
                "🟢 High Match",
                high_count
            )

        with col3:
            st.metric(
                "🟡 Medium Match",
                medium_count
            )

        with col4:
            st.metric(
                "🔴 Low Match",
                low_count
            )


        st.divider()


        # ---------------------------------------------
        # JOB CARDS
        # ---------------------------------------------

        if not displayed_jobs:

            st.warning(
                "No jobs match your selected filters."
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

                badge = get_priority_badge(
                    priority
                )

                title = job.get(
                    "title",
                    "Unknown Job"
                )

                company = job.get(
                    "company",
                    "Unknown Company"
                )

                location = job.get(
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


                # ---------------------------------
                # JOB CONTAINER
                # ---------------------------------

                with st.container(border=True):

                    left, right = st.columns(
                        [4, 1]
                    )


                    # LEFT SIDE

                    with left:

                        st.markdown(
                            f"### 💼 {title}"
                        )

                        st.write(
                            f"**🏢 Company:** {company}"
                        )

                        st.write(
                            f"**📍 Location:** {location}"
                        )

                        st.write(
                            f"**🎯 {get_score_label(score)}**"
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


                    # RIGHT SIDE

                    with right:

                        st.metric(
                            "Match",
                            f"{score}%"
                        )

                        st.write(badge)

                        if url:

                            st.link_button(
                                "🚀 Apply Now",
                                url,
                                use_container_width=True
                            )

                        st.caption(
                            f"Source: {source}"
                        )


                    st.divider()


else:

    # ---------------------------------------------
    # INITIAL SCREEN
    # ---------------------------------------------

    st.info(
        "👆 Click **Search Jobs** to discover "
        "current opportunities matching your profile."
    )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "💼 AI Job Seeker • "
    "AI-powered job discovery and application assistant"
)
