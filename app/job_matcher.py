from typing import Dict, List


def calculate_match_score(job: Dict, profile: Dict) -> int:
    title = str(job.get("title", "")).lower()
    description = str(job.get("description", "")).lower()
    company = str(job.get("company", "")).lower()

    job_text = f"{title} {description} {company}"

    score = 0

    # Strong priority: preferred job roles
    for role in profile.get("preferred_roles", []):
        role_text = role.lower()

        if role_text in title:
            score += 20
        elif role_text in job_text:
            score += 10

    # Preferred domains
    for domain in profile.get("preferred_domains", []):
        if domain.lower() in job_text:
            score += 8

    # Technical skills
    for skill in profile.get("skills", []):
        skill_text = skill.lower()

        # Avoid false matching for one-letter skills such as C
        if len(skill_text) <= 1:
            continue

        if skill_text in job_text:
            score += 4

    # Fresher / graduate friendly keywords
    fresher_keywords = [
        "fresher",
        "graduate",
        "entry level",
        "entry-level",
        "trainee",
        "intern",
        "0-1 years",
        "0-2 years",
        "fresh graduate",
    ]

    for keyword in fresher_keywords:
        if keyword in job_text:
            score += 5

    return min(score, 100)


def classify_job(score: int) -> str:
    if score >= 80:
        return "HIGH"
    elif score >= 60:
        return "MEDIUM"
    else:
        return "LOW"


def analyze_job(job: Dict, profile: Dict) -> Dict:
    score = calculate_match_score(job, profile)

    return {
        **job,
        "match_score": score,
        "priority": classify_job(score),
    }
