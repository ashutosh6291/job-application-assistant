"""
Job matching and scoring engine.
"""

from typing import Dict, List


def calculate_match_score(job: Dict, profile: Dict) -> int:
    """
    Calculate a basic match score between a job and the candidate profile.
    """

    job_text = " ".join([
        str(job.get("title", "")),
        str(job.get("description", "")),
        str(job.get("company", "")),
    ]).lower()

    score = 0
    matched_items: List[str] = []

    # Role matching
    for role in profile.get("preferred_roles", []):
        if role.lower() in job_text:
            score += 15
            matched_items.append(role)

    # Domain matching
    for domain in profile.get("preferred_domains", []):
        if domain.lower() in job_text:
            score += 10
            matched_items.append(domain)

    # Skill matching
    for skill in profile.get("skills", []):
        if skill.lower() in job_text:
            score += 5
            matched_items.append(skill)

    # Cap score at 100
    score = min(score, 100)

    return score


def classify_job(score: int) -> str:
    """
    Convert a numerical score into a priority level.
    """

    if score >= 80:
        return "HIGH"
    elif score >= 60:
        return "MEDIUM"
    else:
        return "LOW"


def analyze_job(job: Dict, profile: Dict) -> Dict:
    """
    Return the job together with its match score and priority.
    """

    score = calculate_match_score(job, profile)

    return {
        **job,
        "match_score": score,
        "priority": classify_job(score),
    }
