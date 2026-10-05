"""
Job search module.

This module will collect relevant job opportunities
from supported job sources.
"""

from typing import List, Dict


def search_jobs(keywords: List[str]) -> List[Dict]:
    """
    Search for jobs using the supplied keywords.

    The actual job-source integrations will be added
    in the next development stage.
    """

    jobs = []

    for keyword in keywords:
        jobs.append({
            "title": keyword,
            "company": "To be discovered",
            "location": "India",
            "url": "",
            "source": "",
        })

    return jobs


if __name__ == "__main__":
    keywords = [
        "Graduate Engineer Trainee",
        "GET Metallurgy",
        "Graduate Engineer",
        "Data Analyst Intern",
        "Banking Operations Analyst",
    ]

    results = search_jobs(keywords)

    for job in results:
        print(job)
