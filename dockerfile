# Usa uma imagem leve do Python 3.10
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências para o container
COPY requirements.txt .

# Instala os pacotes necessários
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte (pasta src/) para dentro do container
COPY ./src ./src

# Copia o arquivo principal que inicia o serviço
COPY main.py .

# Adiciona o diretório base ao PYTHONPATH
ENV PYTHONPATH=/app

# Executa o serviço com o Python
CMD ["python", "main.py"]
