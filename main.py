from src.services.rabbitmq_consumer import start_consumer
from src.controllers.rabbitmq_controller import process_message

if __name__ == "__main__":
    # Inicia o consumidor e executa process_message para cada mensagem recebida da fila
    start_consumer(process_message)
