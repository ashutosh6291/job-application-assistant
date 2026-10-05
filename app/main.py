import sys

from job_matcher import analyze_job
from job_search import search_jobs
from job_storage import save_jobs
from resume_parser import build_candidate_profile


def main():
    if len(sys.argv) < 2:
        print("Usage: python app/main.py <resume.txt>")
        return

    resume_path = sys.argv[1]

    try:
        with open(resume_path, "r", encoding="utf-8") as file:
            resume_text = file.read()
    except OSError as error:
        print(f"Could not read resume: {error}")
        return

    profile = build_candidate_profile(resume_text)

    print("Searching for jobs...")
    jobs = search_jobs()

    print(f"Jobs found: {len(jobs)}")

    analyzed_jobs = []

    for job in jobs:
        result = analyze_job(job, profile)
        analyzed_jobs.append(result)

    analyzed_jobs.sort(
        key=lambda job: job["match_score"],
        reverse=True
    )

    save_jobs(analyzed_jobs)

    print("\nTop matching jobs:\n")

    for job in analyzed_jobs[:20]:
        print("=" * 60)
        print(f"Job: {job['title']}")
        print(f"Company: {job['company']}")
        print(f"Location: {job['location']}")
        print(f"Match Score: {job['match_score']}%")
        print(f"Priority: {job['priority']}")
        print(f"Source: {job['source']}")
        print(f"Apply: {job['url']}")


if __name__ == "__main__":
    main()
