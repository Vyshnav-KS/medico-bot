
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://admin:medulla-poc@medulla-poc.qeuy53j.mongodb.net/?retryWrites=true&w=majority&appName=medulla-poc"

def get_db_connection():
    """
    Establishes a connection to the MongoDB database.
    
    Returns:
        db: MongoDB database instance
    """
    try:
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client["medulla_chat"]
        return db
    except Exception as e:
        print(f"Database configuration error: {e}")
        raise