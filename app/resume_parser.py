import re


COMMON_SKILLS = [
    "Python",
    "C",
    "C++",
    "Java",
    "JavaScript",
    "TypeScript",
    "SQL",
    "Excel",
    "Power BI",
    "Tableau",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
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
    "Process Engineering",
    "Root Cause Analysis",
    "Six Sigma",
]


ROLE_KEYWORDS = [
    "Graduate Engineer Trainee",
    "GET",
    "Graduate Engineer",
    "Trainee Engineer",
    "Management Trainee",
    "Quality Engineer",
    "Production Engineer",
    "Process Engineer",
    "Metallurgy Engineer",
    "Materials Engineer",
    "Manufacturing Engineer",
    "Data Analyst",
    "Data Analyst Intern",
    "Business Analyst",
    "Software Engineer",
    "Research Assistant",
    "Research Intern",
]


DOMAIN_KEYWORDS = {
    "Metallurgy / Materials": [
        "metallurgy",
        "metallurgical",
        "materials science",
        "steel",
        "alloy",
        "metal processing",
    ],

    "Manufacturing": [
        "manufacturing",
        "production",
        "plant",
        "process engineering",
    ],

    "Quality": [
        "quality control",
        "quality assurance",
        "quality engineer",
        "inspection",
    ],

    "Data Analytics": [
        "data analyst",
        "data analysis",
        "analytics",
        "power bi",
        "pandas",
        "sql",
    ],

    "IT / Software": [
        "software engineer",
        "software development",
        "developer",
        "programming",
        "python",
        "java",
        "javascript",
    ],

    "Banking / Finance": [
        "banking",
        "finance",
        "financial",
        "credit",
        "bank",
    ],

    "Research": [
        "research",
        "research assistant",
        "research intern",
        "laboratory",
    ],
}


def normalize_text(text):
    """Normalize resume text."""

    text = str(text or "").lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def contains_keyword(text, keyword):
    """Safely check whether a keyword exists."""

    keyword = normalize_text(keyword)

    if len(keyword) <= 2:

        return bool(
            re.search(
                rf"(?<![a-z0-9])"
                rf"{re.escape(keyword)}"
                rf"(?![a-z0-9])",
                text
            )
        )

    return keyword in text


def extract_skills(resume_text):
    """Extract known technical and domain skills."""

    text = normalize_text(resume_text)

    skills = []

    for skill in COMMON_SKILLS:

        if contains_keyword(text, skill):

            skills.append(skill)

    return skills


def extract_roles(resume_text):
    """Identify roles relevant to the candidate."""

    text = normalize_text(resume_text)

    roles = []

    for role in ROLE_KEYWORDS:

        if contains_keyword(text, role):

            roles.append(role)

    return roles


def extract_domains(resume_text):
    """Identify career domains from the resume."""

    text = normalize_text(resume_text)

    domains = []

    for domain, keywords in DOMAIN_KEYWORDS.items():

        if any(
            contains_keyword(text, keyword)
            for keyword in keywords
        ):

            domains.append(domain)

    return domains


def extract_education(resume_text):
    """Extract basic education information."""

    text = normalize_text(resume_text)

    education = {
        "degree": "",
        "branch": "",
        "college": "",
        "graduation_year": "",
        "cgpa": "",
    }

    # Degree
    degree_patterns = [
        "b.tech",
        "btech",
        "b.e.",
        "b.e",
        "be",
        "m.tech",
        "mtech",
        "m.e.",
        "m.e",
        "b.sc",
        "bsc",
        "m.sc",
        "msc",
        "bba",
        "bca",
        "mba",
        "mca",
    ]

    for degree in degree_patterns:

        if contains_keyword(text, degree):

            education["degree"] = degree.upper()

            break

    # Graduation year
    years = re.findall(
        r"\b(20\d{2})\b",
        text
    )

    if years:

        education["graduation_year"] = years[-1]

    # CGPA
    cgpa_match = re.search(
        r"(?:cgpa|cpi)"
        r"\s*[:\-]?\s*"
        r"([0-9]+(?:\.[0-9]+)?)",
        text
    )

    if cgpa_match:

        education["cgpa"] = cgpa_match.group(1)

    return education


def build_candidate_profile(resume_text):
    """
    Build a candidate profile from the uploaded resume.
    """

    skills = extract_skills(
        resume_text
    )

    roles = extract_roles(
        resume_text
    )

    domains = extract_domains(
        resume_text
    )

    education = extract_education(
        resume_text
    )

    # If no roles were detected, keep broad
    # graduate roles available.

    if not roles:

        roles = [
            "Graduate Engineer",
            "Trainee",
            "Intern",
        ]

    return {
        "education": education,

        "preferred_roles": roles,

        "preferred_domains": domains,

        "skills": skills,

        "experience": [],
    }
