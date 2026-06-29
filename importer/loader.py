import csv

from config import (
    SKILLS_FILE,
    INDUSTRIES_FILE,
    COMPANIES_FILE,
    JOB_SKILLS_FILE,
    JOB_INDUSTRIES_FILE,
    BENEFITS_FILE,
    COMPANY_SPECIALITIES_FILE,
    EMPLOYEE_COUNTS_FILE,
    SALARIES_FILE,
    COMPANY_INDUSTRIES_FILE,
)

#ovaj loader ne uzima postings jer cu njega kasnije
#takodje nema company_industries.csv jer mi nije relevantno za hr upite

def read_csv(file_path):
    rows = []

    with open(file_path, encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            rows.append(row)

    return rows


def load_skills():
    rows = read_csv(SKILLS_FILE)
    return {row["skill_abr"]: row["skill_name"] for row in rows}


def load_industries():
    rows = read_csv(INDUSTRIES_FILE)
    return {row["industry_id"]: row["industry_name"] for row in rows}


def load_companies():
    rows = read_csv(COMPANIES_FILE)
    return {row["company_id"]: row for row in rows}


def load_job_skills():
    rows = read_csv(JOB_SKILLS_FILE)
    job_skills = {}

    for row in rows:
        job_id = row["job_id"]
        skill_abr = row["skill_abr"]

        job_skills.setdefault(job_id, [])

        if skill_abr not in job_skills[job_id]:
            job_skills[job_id].append(skill_abr)

    return job_skills


def load_job_industries():
    rows = read_csv(JOB_INDUSTRIES_FILE)
    job_industries = {}

    for row in rows:
        job_id = row["job_id"]
        industry_id = row["industry_id"]

        job_industries.setdefault(job_id, [])

        if industry_id not in job_industries[job_id]:
            job_industries[job_id].append(industry_id)

    return job_industries


def load_benefits():
    rows = read_csv(BENEFITS_FILE)
    benefits = {}

    for row in rows:
        job_id = row["job_id"]

        benefit = {
            "type": row["type"],
            "inferred": row["inferred"],
        }

        benefits.setdefault(job_id, [])

        if benefit not in benefits[job_id]:
            benefits[job_id].append(benefit)

    return benefits


def load_company_specialities():
    rows = read_csv(COMPANY_SPECIALITIES_FILE)
    specialities = {}

    for row in rows:
        company_id = row["company_id"]
        speciality = row["speciality"]

        specialities.setdefault(company_id, [])

        if speciality not in specialities[company_id]:
            specialities[company_id].append(speciality)

    return specialities


def load_latest_employee_counts():
    rows = read_csv(EMPLOYEE_COUNTS_FILE)
    latest_counts = {}

    for row in rows:
        company_id = row["company_id"]
        time_recorded = int(row["time_recorded"]) if row["time_recorded"] else 0

        if company_id not in latest_counts:
            latest_counts[company_id] = row
            continue

        existing_time = int(latest_counts[company_id]["time_recorded"])

        if time_recorded > existing_time:
            latest_counts[company_id] = row

    return latest_counts


def load_salaries():
    rows = read_csv(SALARIES_FILE)
    salaries = {}

    for row in rows:
        job_id = row["job_id"]

        salaries[job_id] = row

    return salaries

def load_company_industries():
    rows = read_csv(COMPANY_INDUSTRIES_FILE)
    company_industries = {}

    for row in rows:
        company_id = row["company_id"]
        industry = row["industry"]

        company_industries.setdefault(company_id, [])

        if industry not in company_industries[company_id]:
            company_industries[company_id].append(industry)

    return company_industries