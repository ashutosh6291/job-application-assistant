# 🤖 AI Job Seeker

> An AI-powered job discovery and matching platform that helps candidates find relevant opportunities based on their resume, preferred location, and career domain.

## 🚀 Live Demo

👉 [**Launch AI Job Seeker**](https://job-application-assistant-8cbdpemhzlgwjjcqojagww.streamlit.app/)

## ✨ Features

- 📄 Upload your own PDF resume
- 🤖 Automatically analyze resume skills and career domains
- 🔎 Search current job opportunities
- 🎯 Match jobs against the candidate's resume
- 📊 AI-based job match scoring
- 🟢 High / 🟡 Medium / 🔴 Low match classification
- 💡 Explain why a job matches the candidate
- 📍 Filter jobs by location
- 🏢 Filter jobs by career domain
- 🚀 Direct links to original job postings
- 👥 Designed for multiple job seekers
- 🔐 No hardcoded candidate profile required

## 🎯 Supported Career Areas

- Graduate Engineer / GET
- Trainee Engineer
- Metallurgy & Materials
- Manufacturing
- Quality
- Production
- Process Engineering
- Data Analytics
- IT / Software
- Banking / Finance
- Research
- Internships
- Apprenticeships

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Sentence Transformers
- PyPDF
- REST APIs
- GitHub

## ⚙️ How It Works

1. **Upload Resume**
   - Upload a PDF resume.

2. **Resume Analysis**
   - The system extracts skills, roles, education information, and career domains.

3. **Choose Preferences**
   - Select preferred location and career domain.

4. **Job Search**
   - The system retrieves available job opportunities.

5. **AI Matching**
   - Jobs are analyzed against the candidate's resume.

6. **Ranked Results**
   - Jobs are sorted according to their match score.

7. **Apply**
   - Candidates can open the original job posting and apply.

## 📁 Project Structure

```text
job-application-assistant/
│
├── app/
│   ├── job_matcher.py
│   ├── job_search.py
│   ├── job_storage.py
│   ├── main.py
│   ├── profile.py
│   ├── resume_parser.py
│   └── streamlit_app.py
│
├── web/
├── requirements.txt
├── .gitignore
└── README.md
