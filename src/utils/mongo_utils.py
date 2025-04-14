from pymongo import MongoClient
from src.config.settings import MONGO_URI, MONGO_DB, MONGO_COLLECTION

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

def enrich_data(data):
    for row in data:
        cpf = row.get("CPF")
        if cpf:
            enriched_info = collection.find_one({"CPF": cpf})
            if enriched_info:
                row.update(enriched_info)  # Adiciona os dados do MongoDB à linha
    return data
