"""
Job Application Assistant
Main application entry point.
"""

from profile import PROFILE
from job_matcher import analyze_job


def main():

    sample_jobs = [
        {
            "title": "Graduate Engineer Trainee - Metallurgy",
            "company": "Example Steel Company",
            "location": "India",
            "description": """
            B.Tech in Metallurgy or Materials Engineering.
            Graduate Engineer Trainee role in steel manufacturing,
            quality control and production processes.
            Knowledge of metallurgy and quality analysis preferred.
            """,
            "url": "https://example.com/job1",
        },

        {
            "title": "Data Analyst Intern",
            "company": "Example Technology Company",
            "location": "India",
            "description": """
            Looking for candidates with Python, SQL, Pandas,
            NumPy and data analysis skills.
            """,
            "url": "https://example.com/job2",
        },

        {
            "title": "Marketing Executive",
            "company": "Example Company",
            "location": "India",
            "description": """
            Sales and marketing position.
            Excellent communication skills required.
            """,
            "url": "https://example.com/job3",
        },
    ]

    print("=" * 70)
    print("JOB APPLICATION ASSISTANT")
    print("=" * 70)

    for job in sample_jobs:

        result = analyze_job(job, PROFILE)

        print()
        print(f"Job: {result['title']}")
        print(f"Company: {result['company']}")
        print(f"Location: {result['location']}")
        print(f"Match Score: {result['match_score']}%")
        print(f"Priority: {result['priority']}")
        print(f"URL: {result['url']}")
        print("-" * 70)


if __name__ == "__main__":
    main()
