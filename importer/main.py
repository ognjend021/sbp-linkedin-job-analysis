from config import POSTINGS_FILE
from loader import (
    read_csv,
    load_skills,
    load_industries,
    load_companies,
    load_job_skills,
    load_job_industries,
    load_benefits,
    load_latest_employee_counts,
    load_company_specialities,
    load_company_industries,
)
from builder import build_all_documents
from database import get_database, drop_collections, insert_documents


def main():
    print("Povezivanje sa MongoDB bazom...")
    db = get_database()

    print("Učitavanje CSV podataka...")
    postings = read_csv(POSTINGS_FILE)

    documents = build_all_documents(
        postings=postings,
        companies_map=load_companies(),
        skill_map=load_skills(),
        industry_map=load_industries(),
        job_skills_map=load_job_skills(),
        job_industries_map=load_job_industries(),
        benefits_map=load_benefits(),
        employee_counts_map=load_latest_employee_counts(),
        specialities_map=load_company_specialities(),
        company_industries_map=load_company_industries(),
    )

    print("Brisanje postojećih kolekcija...")
    drop_collections(db)

    print("Ubacivanje dokumenata u MongoDB...")
    insert_documents(
        db=db,
        companies=documents["companies"],
        job_metadata=documents["job_metadata"],
        job_postings=documents["job_postings"],
    )

    print("Import završen.")
    print(f"job_postings: {len(documents['job_postings'])}")
    print(f"job_metadata: {len(documents['job_metadata'])}")
    print(f"companies: {len(documents['companies'])}")


if __name__ == "__main__":
    main()