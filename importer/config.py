from pathlib import Path

# Root direktorijum projekta
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Folder sa CSV datotekama
DATA_DIR = PROJECT_ROOT / "data"

# MongoDB
DATABASE_NAME = "linkedin_jobs"

COLLECTION_JOB_POSTINGS = "job_postings"
COLLECTION_COMPANIES = "companies"
COLLECTION_JOB_METADATA = "job_metadata"

# CSV datoteke
POSTINGS_FILE = DATA_DIR / "postings.csv"
COMPANIES_FILE = DATA_DIR / "companies.csv"
EMPLOYEE_COUNTS_FILE = DATA_DIR / "employee_counts.csv"
COMPANY_SPECIALITIES_FILE = DATA_DIR / "company_specialities.csv"

SKILLS_FILE = DATA_DIR / "skills.csv"
JOB_SKILLS_FILE = DATA_DIR / "job_skills.csv"

INDUSTRIES_FILE = DATA_DIR / "industries.csv"
JOB_INDUSTRIES_FILE = DATA_DIR / "job_industries.csv"

BENEFITS_FILE = DATA_DIR / "benefits.csv"

SALARIES_FILE = DATA_DIR / "salaries.csv"

COMPANY_INDUSTRIES_FILE = DATA_DIR / "company_industries.csv"