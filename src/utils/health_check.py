import os
import logging
import pika
import requests
from pymongo import MongoClient
from requests.auth import HTTPBasicAuth

# 🎨 Funções para colorir o terminal
def color(msg, code): return f"\033[{code}m{msg}\033[0m"
SUCCESS = lambda msg: color(msg, "92")   # Verde
WARNING = lambda msg: color(msg, "93")   # Amarelo
ERROR   = lambda msg: color(msg, "91")   # Vermelho
INFO    = lambda msg: color(msg, "94")   # Azul

# 📝 Configura o log em arquivo
logging.basicConfig(
    filename="health_check.log",
    filemode="a",
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)

def test_rabbitmq():
    print(INFO("🔍 Testando conexão com RabbitMQ..."))
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
        print(SUCCESS("✅ Conectado ao RabbitMQ e fila verificada!"))
        logging.info("RabbitMQ conectado e fila verificada.")
        connection.close()
    except Exception as e:
        print(ERROR(f"❌ Erro ao conectar no RabbitMQ: {e}"))
        logging.error(f"Erro RabbitMQ: {e}")

def test_owncloud():
    print(INFO("🔍 Testando acesso ao OwnCloud via WebDAV..."))
    try:
        url = os.getenv("OWNCLOUD_URL")
        auth = HTTPBasicAuth(os.getenv("OWNCLOUD_USER"), os.getenv("OWNCLOUD_PASS"))
        response = requests.request("PROPFIND", url, auth=auth, timeout=10)

        if response.status_code in [207, 200]:
            print(SUCCESS("✅ OwnCloud acessível via WebDAV!"))
            logging.info("OwnCloud acessível via WebDAV.")
        else:
            print(WARNING(f"❌ Resposta inesperada do OwnCloud: {response.status_code}"))
            logging.warning(f"Resposta inesperada OwnCloud: {response.status_code}")
    except Exception as e:
        print(ERROR(f"❌ Erro ao acessar o OwnCloud: {e}"))
        logging.error(f"Erro OwnCloud: {e}")

def test_mongodb():
    print(INFO("🔍 Testando conexão com MongoDB..."))
    try:
        client = MongoClient(os.getenv("MONGO_URI"), serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        db = client[os.getenv("MONGO_DB")]
        collection = db[os.getenv("MONGO_COLLECTION")]
        doc = collection.find_one()
        if doc:
            print(SUCCESS("✅ MongoDB conectado! Coleção contém documentos."))
            logging.info("MongoDB conectado com documentos.")
        else:
            print(WARNING("⚠️ MongoDB conectado, mas a coleção está vazia."))
            logging.warning("MongoDB conectado, coleção vazia.")
    except Exception as e:
        print(ERROR(f"❌ Erro ao conectar no MongoDB: {e}"))
        logging.error(f"Erro MongoDB: {e}")

# 🔄 Wrapper para executar tudo
def run_health_check_on_startup():
    print("\n🚦 Iniciando verificação de saúde do pyService...\n")
    test_rabbitmq()
    test_owncloud()
    test_mongodb()
    print("\n✅ Verificação concluída.\n")

# 🎯 Execução manual direta via terminal
if __name__ == "__main__":
    run_health_check_on_startup()


'''
Para executar esse script de teste no terminal linux digite dentro da pasta do projeto:
docker exec -it pyservice bash
Acesse o diretório em que o arquivo send_test_message.py está:
cd src/utils
Depois digite:
python health_check.py
'''

'''
Para executar esse script de teste no terminal linux digite dentro da pasta do projeto:
docker exec -it pyservice bash (para acessar o bash do container pyservice)
Acesse o diretório em que o arquivo send_test_message.py está:
cd src/utils
Depois digite:
python health_check.py
'''