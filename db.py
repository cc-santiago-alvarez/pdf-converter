from pymongo import MongoClient
from bson import errors

def get_db_connection():
    try:
        client = MongoClient(
            "mongodb://xxxxxxx@localhost:27017"
        )
        return client.database
    except errors.ConnectionFailure as e:
        raise ConnectionError(f"Error de conexión: {str(e)}")