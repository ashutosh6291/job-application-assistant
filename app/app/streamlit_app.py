import streamlit as st
from job_search import search_jobs
from job_matcher import analyze_job
from profile import PROFILE


st.set_page_config(
    page_title="AI Job Seeker",
    page_icon="💼",
    layout="wide"
)


st.title("💼 AI Job Seeker")
st.subheader("Find jobs that match your profile")

st.write(
    "AI-powered job search for GET, Graduate Engineer, "
    "Trainee, Data Analyst and Banking opportunities."
)

st.divider()


# Sidebar
st.sidebar.header("🎯 Job Preferences")

show_high_only = st.sidebar.checkbox(
    "Show HIGH priority jobs only",
    value=False
)

max_jobs = st.sidebar.slider(
    "Number of jobs",
    min_value=5,
    max_value=50,
    value=20
)


# Profile section
with st.expander("👤 My Profile"):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("**Degree:**", PROFILE["education"]["degree"])
        st.write("**Branch:**", PROFILE["education"]["branch"])

    with col2:
        st.write("**College:**", PROFILE["education"]["college"])
        st.write("**Graduation:**", PROFILE["education"]["graduation_year"])

    with col3:
        st.write("**CGPA:**", PROFILE["education"]["cgpa"])


# Search button
if st.button("🔎 Search Jobs", type="primary"):

    with st.spinner("Searching for jobs..."):

        jobs = search_jobs()

        if not jobs:
            st.warning(
                "No jobs were returned by the job source. "
                "Please try again later."
            )
        else:

            analyzed_jobs = []

            for job in jobs:
                result = analyze_job(job, PROFILE)
                analyzed_jobs.append(result)

            # Sort by match score
            analyzed_jobs.sort(
                key=lambda x: x.get("match_score", 0),
                reverse=True
            )

            # Filter
            if show_high_only:
                analyzed_jobs = [
                    job for job in analyzed_jobs
                    if job.get("priority") == "HIGH"
                ]

            analyzed_jobs = analyzed_jobs[:max_jobs]

            st.success(
                f"Found {len(jobs)} jobs. "
                f"Showing {len(analyzed_jobs)} best matches."
            )

            st.divider()

            # Display jobs
            for job in analyzed_jobs:

                score = job.get("match_score", 0)
                priority = job.get("priority", "LOW")

                if priority == "HIGH":
                    badge = "🟢 HIGH"
                elif priority == "MEDIUM":
                    badge = "🟡 MEDIUM"
                else:
                    badge = "🔴 LOW"

                with st.container():

                    col1, col2 = st.columns([4, 1])

                    with col1:

                        st.markdown(
                            f"### {job.get('title', 'Unknown Job')}"
                        )

                        st.write(
                            f"**🏢 Company:** "
                            f"{job.get('company', 'Unknown')}"
                        )

                        st.write(
                            f"**📍 Location:** "
                            f"{job.get('location', 'Not specified')}"
                        )

                        st.write(
                            f"**📊 Match Score:** "
                            f"{score}/100"
                        )

                        description = job.get(
                            "description",
                            ""
                        )

                        if description:
                            clean_description = (
                                description
                                .replace("<br>", " ")
                                .replace("<p>", " ")
                                .replace("</p>", " ")
                            )

                            st.write(
                                clean_description[:500] + "..."
                            )

                    with col2:

                        st.metric(
                            "Match",
                            f"{score}%"
                        )

                        st.write(badge)

                        url = job.get("url", "")

                        if url:
                            st.link_button(
                                "🚀 Apply",
                                url
                            )

                        st.caption(
                            f"Source: {job.get('source', 'Unknown')}"
                        )

                    st.divider()


else:

    st.info(
        "Click **Search Jobs** to find current opportunities "
        "matching your profile."
    )


st.caption(
    "AI Job Seeker • Job matching and application preparation assistant"
)
