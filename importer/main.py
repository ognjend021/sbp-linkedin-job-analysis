from loader import (
    load_skills,
    load_industries,
    load_companies,
    load_job_skills,
    load_job_industries,
    load_benefits,
    load_company_specialities,
    load_latest_employee_counts,
    load_salaries,
    load_company_industries,
)


def main():
    skill_map = load_skills()
    industry_map = load_industries()
    company_map = load_companies()

    job_skills_map = load_job_skills()
    job_industries_map = load_job_industries()
    benefits_map = load_benefits()
    specialities_map = load_company_specialities()

    employee_counts_map = load_latest_employee_counts()
    salary_map = load_salaries()

    company_industries_map = load_company_industries()

    print(f"Broj učitanih veština: {len(skill_map)}")
    print(f"Broj učitanih industrija: {len(industry_map)}")
    print(f"Broj učitanih kompanija: {len(company_map)}")

    print(f"Broj oglasa sa veštinama: {len(job_skills_map)}")
    print(f"Broj oglasa sa industrijama: {len(job_industries_map)}")
    print(f"Broj oglasa sa benefitima: {len(benefits_map)}")
    print(f"Broj kompanija sa specijalizacijama: {len(specialities_map)}")

    print(f"Broj kompanija sa employee_count podacima: {len(employee_counts_map)}")
    print(f"Broj oglasa sa salary podacima: {len(salary_map)}")

    print(f"Broj kompanija sa industrijama: {len(company_industries_map)}")


if __name__ == "__main__":
    main()