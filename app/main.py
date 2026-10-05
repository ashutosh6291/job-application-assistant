from profile import PROFILE
from job_matcher import analyze_job
from job_search import search_jobs
from job_storage import save_jobs


def main():
    print("Searching for jobs...")
    jobs = search_jobs()

    print(f"Jobs found: {len(jobs)}")

    analyzed_jobs = []

    for job in jobs:
        result = analyze_job(job, PROFILE)
        analyzed_jobs.append(result)

    analyzed_jobs.sort(
        key=lambda job: job["match_score"],
        reverse=True
    )

    # Save all analyzed jobs
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
