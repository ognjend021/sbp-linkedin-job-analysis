from pymongo import MongoClient
from dotenv import load_dotenv
import os

from config import DATABASE_NAME

load_dotenv()

def get_database():
    """
    Vraća konekciju na MongoDB bazu.
    """

    mongo_uri = os.getenv(
        "MONGO_URI",
        "mongodb://localhost:27017"
    )

    client = MongoClient(mongo_uri)

    return client[DATABASE_NAME]