import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# RabbitMQ
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "file_processing")  # valor padrão

# MongoDB
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

# OwnCloud

OWNCLOUD_URL = os.getenv("OWNCLOUD_URL")
OWNCLOUD_USER = os.getenv("OWNCLOUD_USER")
OWNCLOUD_PASS = os.getenv("OWNCLOUD_PASS")
REMOTE_WORK_DIR = os.getenv("OWNCLOUD_WORK_DIR")
REMOTE_FINALIZED_DIR = os.getenv("OWNCLOUD_FINAL_DIR")
# Diretórios locais
WORK_DIR =  Path("work/")
FINALIZED_DIR = Path("finalizado/")

# Validação básica (opcional, mas recomendado)
required_vars = {
    "RABBITMQ_HOST": RABBITMQ_HOST,
    "MONGO_URI": MONGO_URI,
    "MONGO_DB": MONGO_DB,
    "MONGO_COLLECTION": MONGO_COLLECTION,
    "OWNCLOUD_URL": OWNCLOUD_URL,
    "OWNCLOUD_USER": OWNCLOUD_USER,
    "OWNCLOUD_PASS": OWNCLOUD_PASS,
}

for var, value in required_vars.items():
    if not value:
        raise EnvironmentError(f"Variável de ambiente obrigatória não definida: {var}")
