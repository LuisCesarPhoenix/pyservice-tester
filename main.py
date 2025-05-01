import logging
# Importa o módulo logging para registrar logs no terminal

from src.services.rabbitmq_consumer import start_consumer
# Importa a função que inicia o consumidor RabbitMQ

from src.controllers.rabbitmq_controller import process_message
# Importa a função que processa cada mensagem da fila

from src.utils.health_check import run_health_check_on_startup
# Importa a função que executa a verificação de saúde na inicialização

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
# Configura o formato e o nível dos logs para exibir informações no terminal

try:
    run_health_check_on_startup()
    # Tenta executar a verificação de saúde ao iniciar o serviço
    logging.info("✅ Verificação de saúde concluída com sucesso.")
except Exception as e:
    logging.error(f"❌ Erro na verificação de saúde: {e}")
    # Se ocorrer um erro durante a verificação de saúde, exibe no log
    raise

if __name__ == "__main__":
    # Verifica se o script está sendo executado diretamente (não importado)

    try:
        logging.info("🚀 Iniciando consumidor RabbitMQ...")
        start_consumer(process_message)
        # Inicia o consumidor e processa mensagens da fila usando a função process_message
    except Exception as e:
        logging.critical(f"🔥 Erro crítico ao iniciar o consumidor RabbitMQ: {e}")
        # Em caso de falha ao iniciar o consumidor, registra um erro crítico
        raise
