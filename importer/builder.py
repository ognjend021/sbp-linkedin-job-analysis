from datetime import datetime


def to_int(value):
    if value is None or value == "":
        return None

    try:
        return int(float(value))
    except ValueError:
        return None


def to_float(value):
    if value is None or value == "":
        return None

    try:
        return float(value)
    except ValueError:
        return None


def to_bool(value):
    if value is None or value == "":
        return None

    value = str(value).strip().lower()

    if value in ["true", "1", "yes"]:
        return True

    if value in ["false", "0", "no"]:
        return False

    return None


def to_datetime_from_timestamp(value):
    if value is None or value == "":
        return None

    try:
        timestamp = int(float(value))
        return datetime.fromtimestamp(timestamp / 1000)
    except ValueError:
        return None


def build_job_posting(row):
    return {
        "job_id": to_int(row.get("job_id")),
        "company_id": to_int(row.get("company_id")),

        "title": row.get("title"),
        "description": row.get("description"),

        "formatted_work_type": row.get("formatted_work_type"),
        "work_type": row.get("work_type"),
        "formatted_experience_level": row.get("formatted_experience_level"),

        "location": row.get("location"),
        "zip_code": row.get("zip_code"),
        "fips": row.get("fips"),

        "remote_allowed": to_bool(row.get("remote_allowed")),
        "sponsored": to_bool(row.get("sponsored")),

        "salary": {
            "min_salary": to_float(row.get("min_salary")),
            "med_salary": to_float(row.get("med_salary")),
            "max_salary": to_float(row.get("max_salary")),
            "normalized_salary": to_float(row.get("normalized_salary")),
            "currency": row.get("currency"),
            "pay_period": row.get("pay_period"),
            "compensation_type": row.get("compensation_type"),
        },

        "metrics": {
            "views": to_int(row.get("views")),
            "applies": to_int(row.get("applies")),
        },

        "dates": {
            "listed_time": to_datetime_from_timestamp(row.get("listed_time")),
            "original_listed_time": to_datetime_from_timestamp(row.get("original_listed_time")),
            "expiry": to_datetime_from_timestamp(row.get("expiry")),
            "closed_time": to_datetime_from_timestamp(row.get("closed_time")),
        },
    }


def build_job_metadata(row, skill_map, industry_map, job_skills_map, job_industries_map, benefits_map):
    job_id = row.get("job_id")

    skills = []
    for skill_abr in job_skills_map.get(job_id, []):
        skills.append({
            "skill_abr": skill_abr,
            "skill_name": skill_map.get(skill_abr),
        })

    industries = []
    for industry_id in job_industries_map.get(job_id, []):
        industries.append({
            "industry_id": to_int(industry_id),
            "industry_name": industry_map.get(industry_id),
        })

    benefits = []
    for benefit in benefits_map.get(job_id, []):
        benefits.append({
            "type": benefit.get("type"),
            "inferred": to_bool(benefit.get("inferred")),
        })

    return {
        "job_id": to_int(job_id),
        "skills": skills,
        "industries": industries,
        "benefits": benefits,
    }


def build_company(row, employee_counts_map, specialities_map, company_industries_map):
    company_id = row.get("company_id")
    employee_data = employee_counts_map.get(company_id, {})

    return {
        "company_id": to_int(company_id),
        "name": row.get("name"),

        "company_size": to_int(row.get("company_size")),

        "country": row.get("country"),
        "state": row.get("state"),
        "city": row.get("city"),
        "address": row.get("address"),

        "employee_count": to_int(employee_data.get("employee_count")),
        "follower_count": to_int(employee_data.get("follower_count")),

        "industries": company_industries_map.get(company_id, []),
        "specialities": specialities_map.get(company_id, []),
    }

def build_all_documents(
    postings,
    companies_map,
    skill_map,
    industry_map,
    job_skills_map,
    job_industries_map,
    benefits_map,
    employee_counts_map,
    specialities_map,
    company_industries_map,
):
    job_postings = []
    job_metadata = []
    companies = []

    for posting_row in postings:
        job_postings.append(build_job_posting(posting_row))

        job_metadata.append(
            build_job_metadata(
                posting_row,
                skill_map,
                industry_map,
                job_skills_map,
                job_industries_map,
                benefits_map,
            )
        )

    for company_row in companies_map.values():
        companies.append(
            build_company(
                company_row,
                employee_counts_map,
                specialities_map,
                company_industries_map,
            )
        )

    return {
        "job_postings": job_postings,
        "job_metadata": job_metadata,
        "companies": companies,
    }