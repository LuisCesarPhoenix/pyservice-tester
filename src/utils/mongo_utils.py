# src/utils/mongodb_utils.py
from pymongo import MongoClient, errors
from src.config.settings import MONGO_URI, MONGO_DB, MONGO_COLLECTION

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.server_info()  # Força verificação de conexão
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
except errors.ServerSelectionTimeoutError as e:
    print(f"[❌] Erro ao conectar ao MongoDB: {e}")
    collection = None


def enrich_data(data):
    """
    Enriquece os dados com base no CPF consultando o MongoDB.
    """
    if not collection:
        print("[!] Coleção do MongoDB não está disponível.")
        return data

    for row in data:
        cpf = row.get("CPF")
        if cpf:
            enriched_info = collection.find_one({"CPF": cpf})
            if enriched_info:
                # Evita sobrescrever dados já existentes no row (como CPF duplicado)
                enriched_info.pop("_id", None)  # Remove o _id do MongoDB
                row.update(enriched_info)
    return data
