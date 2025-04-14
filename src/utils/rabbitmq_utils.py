# src/utils/rabbitmq_utils.py

import pika
import json
from src.config.rabbitmq_config import get_rabbitmq_connection, RABBITMQ_QUEUE

def publish_message(message: dict) -> None:
    """
    Publica uma mensagem na fila do RabbitMQ.
    
    Args:
        message (dict): Dados a serem enviados.
    """
    connection, channel = get_rabbitmq_connection()

    channel.basic_publish(
        exchange="",
        routing_key=RABBITMQ_QUEUE,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2  # Mensagem persistente
        )
    )

    print(f"[x] Mensagem enviada: {message}")
    connection.close()


def consume_queue(callback) -> None:
    """
    Inicia o consumo da fila e executa o callback para cada mensagem recebida.

    Args:
        callback (function): Função a ser executada ao receber uma mensagem.
    """
    connection, channel = get_rabbitmq_connection()

    def on_message(ch, method, properties, body):
        try:
            message = json.loads(body)
            file_path = message.get("file_path")

            if file_path:
                callback(file_path)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            else:
                print("[!] Mensagem inválida: 'file_path' ausente.")
                ch.basic_nack(delivery_tag=method.delivery_tag)

        except Exception as e:
            print(f"[!] Erro ao processar mensagem: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=RABBITMQ_QUEUE,
        on_message_callback=on_message
    )

    print(f"[*] Aguardando mensagens na fila '{RABBITMQ_QUEUE}'. Pressione CTRL+C para sair.")
    channel.start_consuming()
