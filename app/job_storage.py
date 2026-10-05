import json
import os
from typing import Dict, List


DATA_DIR = "data"
JOBS_FILE = os.path.join(DATA_DIR, "jobs.json")


def save_jobs(jobs: List[Dict]) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(JOBS_FILE, "w", encoding="utf-8") as file:
        json.dump(jobs, file, indent=2, ensure_ascii=False)


def load_jobs() -> List[Dict]:
    if not os.path.exists(JOBS_FILE):
        return []

    with open(JOBS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
