# src/services/rabbitmq_consumer.py

from src.utils.rabbitmq_utils import consume_queue

def start_consumer(callback):
    """Inicia o consumidor do RabbitMQ com a função de callback fornecida."""
    consume_queue(callback)
