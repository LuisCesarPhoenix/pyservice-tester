import os
import pika
import requests
from pymongo import MongoClient
from requests.auth import HTTPBasicAuth

def test_rabbitmq():
    print("🔍 Testando conexão com RabbitMQ...")
    try:
        credentials = pika.PlainCredentials(
            os.getenv("RABBITMQ_DEFAULT_USER"), os.getenv("RABBITMQ_DEFAULT_PASS")
        )
        parameters = pika.ConnectionParameters(
            host=os.getenv("RABBITMQ_HOST"),
            port=int(os.getenv("RABBITMQ_PORT")),
            credentials=credentials
        )
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue=os.getenv("RABBITMQ_QUEUE"), durable=True)
        print("✅ Conectado ao RabbitMQ e fila verificada!")
        connection.close()
    except Exception as e:
        print(f"❌ Erro ao conectar no RabbitMQ: {e}")

def test_owncloud():
    print("🔍 Testando acesso ao OwnCloud via WebDAV...")
    try:
        url = os.getenv("OWNCLOUD_URL")
        auth = HTTPBasicAuth(os.getenv("OWNCLOUD_USER"), os.getenv("OWNCLOUD_PASS"))
        response = requests.request("PROPFIND", url, auth=auth, timeout=10)

        if response.status_code in [207, 200]:
            print("✅ OwnCloud acessível via WebDAV!")
        else:
            print(f"❌ Resposta inesperada do OwnCloud: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao acessar o OwnCloud: {e}")

def test_mongodb():
    print("🔍 Testando conexão com MongoDB...")
    try:
        client = MongoClient(os.getenv("MONGO_URI"), serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        # O comando "ping" é instantâneo e só verifica se o MongoDB respondeu — sem acessar coleção ou contar nada.
        db = client[os.getenv("MONGO_DB")]
        collection = db[os.getenv("MONGO_COLLECTION")]
        doc = collection.find_one()
        # Se quiser testar a coleção, use um find_one():
        if doc:
            print("✅ MongoDB conectado! Coleção contém documentos.")
        else:
            print("⚠️ MongoDB conectado, mas a coleção está vazia.")
    except Exception as e:
        print(f"❌ Erro ao conectar no MongoDB: {e}")

if __name__ == "__main__":
    test_rabbitmq()
    test_owncloud()
    test_mongodb()

'''
Para executar esse script de teste no terminal linux digite dentro da pasta do projeto:
docker exec -it pyservice bash
Acesse o diretório em que o arquivo send_test_message.py está:
cd src/utils
Depois digite:
python health_check.py
'''