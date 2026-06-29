from pymongo import MongoClient
from dotenv import load_dotenv
import os

from config import (
    DATABASE_NAME,
    COLLECTION_COMPANIES,
    COLLECTION_JOB_METADATA,
    COLLECTION_JOB_POSTINGS,
)

load_dotenv()


def get_database():
    mongo_uri = os.getenv(
        "MONGO_URI",
        "mongodb://localhost:27017"
    )

    client = MongoClient(mongo_uri)

    return client[DATABASE_NAME]


def drop_collections(db):
    db[COLLECTION_COMPANIES].drop()
    db[COLLECTION_JOB_METADATA].drop()
    db[COLLECTION_JOB_POSTINGS].drop()


def insert_documents(
    db,
    companies,
    job_metadata,
    job_postings,
):
    if companies:
        db[COLLECTION_COMPANIES].insert_many(companies),
        ordered=False

    if job_metadata:
        db[COLLECTION_JOB_METADATA].insert_many(job_metadata),
        ordered=False

    if job_postings:
        db[COLLECTION_JOB_POSTINGS].insert_many(job_postings),
        ordered=False