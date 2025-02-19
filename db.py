from pymongo import MongoClient
from bson import errors

def get_db_connection():
    try:
        client = MongoClient(
            "mongodb://root:12345abc@localhost:27017/futurapps?authSource=admin&directConnection=true"
        )
        return client.futurapps
    except errors.ConnectionFailure as e:
        raise ConnectionError(f"Error de conexión: {str(e)}")