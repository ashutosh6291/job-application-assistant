"""
Real job search module.
"""

import requests
from typing import List, Dict


ARBEITNOW_API = "https://www.arbeitnow.com/api/job-board-api"


def search_arbeitnow() -> List[Dict]:
    """
    Fetch jobs from the Arbeitnow public job API.
    """

    try:
        response = requests.get(
            ARBEITNOW_API,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        return data.get("data", [])

    except requests.RequestException as error:
        print(f"Job API error: {error}")
        return []


def normalize_job(job: Dict) -> Dict:
    """
    Convert an external job listing into our standard format.
    """

    return {
        "title": job.get("title", ""),
        "company": job.get("company_name", ""),
        "location": job.get("location", ""),
        "description": job.get("description", ""),
        "url": job.get("url", ""),
        "source": "Arbeitnow",
    }


def search_jobs() -> List[Dict]:
    """
    Fetch and normalize jobs.
    """

    raw_jobs = search_arbeitnow()

    jobs = []

    for job in raw_jobs:
        jobs.append(normalize_job(job))

    return jobs


if __name__ == "__main__":

    jobs = search_jobs()

    print(f"Jobs found: {len(jobs)}")

    for job in jobs[:10]:
        print()
        print(job["title"])
        print(job["company"])
        print(job["location"])
        print(job["url"])
