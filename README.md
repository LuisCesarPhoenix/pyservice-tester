# Documentação do pyService


## Estrutura do Projeto

#### Diretórios e arquivos principais:
A seguinte estrutura de diretórios e arquivos compõe o projeto pyService:

pyService/  
├── .dockerignore                   # Evita que arquivos desnecessários sejam enviados para o contexto da imagem  
├── .env                            # Arquivo de variáveis de ambiente  
├── .env.example.env                # Arquivo exemplo de variáveis de ambiente  
├── .gitignore                      # Informar ao Git quais arquivos ou diretórios devem ser ignorados (como .env, por exemplo)  
├── anotacoes_pyservice				# Contém anotações do desenvolvedor com ideias, rascunhos, fluxos de trabalho e observações  
├── docker-compose.yml              # Arquivo de configuração do Docker Compose  
├── dockerfile                      # Dockerfile para containerização  
├── main.py                         # Arquivo principal do serviço  
├── README.md                       # Documentação do projeto  
├── requirements.txt                # Dependências do Python  
├── arquivos-para-consulta/ 		# Armazenar arquivos de referência, templates ou modelos para enriquecimento/higienização  
├── src/  
│   ├── config/  
│   │   ├── rabbitmq_config.py      # Configuração da conexão com RabbitMQ  
│   │   ├── settings.py             # Configuração das variáveis de ambiente  
│   ├── controllers/  
│   │   ├── rabbitmq_controller.py  # Processamento de mensagens da fila  
│   ├── models/  
│   │   ├── data_schema.py          # Estrutura dos dados para enriquecimento  
│   ├── routes/  
│   ├── services/  
│   │   ├── file_service.py         # Lógica de higienização e enriquecimento de dados  
│   │   ├── rabbitmq_consumer.py    # Consumidor do RabbitMQ que escuta a fila  
│   │   ├── report_service.py       # Geração de relatórios PDF e dashboards  
│   ├── tests/  
│   │   ├── send_test_message.py 	# Enviar mensagens simuladas para a fila RabbitMQ (teste de integração)  
│   ├── utils/  
│   │   ├── rabbitmq_utils.py       # Envio e recebimento de mensagens do RabbitMQ  
│   │   ├── owncloud_utils.py       # Conexão e manipulação de arquivos no OwnCloud  
│   │   ├── mongo_utils.py          # Conexão e consultas ao MongoDB  
├── storage/                        # Diretório para armazenar arquivos temporários e processados  
│   ├── work/                       # Arquivos aguardando processamento  
│   ├── finalizado/                 # Arquivos processados  
├──  
  
## 🧭 Fluxo Completo:

1.	🌐 API (Node.js):
	a.	Recebe uma requisição para processar um arquivo.
	b.	Envia uma mensagem para o RabbitMQ com os  metadados ou caminho do arquivo.
2.	📬 RabbitMQ:
	a.	Escuta a fila (pyservice_queue).
	b.	Entrega a mensagem para o pyService.
3.	🧠 pyService (Python):
	Ao receber a mensagem:
		a.	Acessa o OwnCloud e pega o arquivo a ser tratado (do diretório /work/).
		b.	Higieniza e enriquece os dados:
			i.	Conecta no MongoDB remoto e busca/completa os dados.
		c.	Salva o arquivo finalizado no OwnCloud (diretório /finalizado/).
		d.	Envia uma mensagem de status para o Strapi, avisando que o processo foi concluído.

## Visão Geral Detalhada:

O pyService é um microsserviço em Python criado para automatizar o processamento inteligente de arquivos CSV em um fluxo completo 
de:
a)Integração com filas de mensagens (RabbitMQ): para saber quando um novo arquivo precisa ser processado.
b)Integração com OwnCloud: para acessar e armazenar arquivos no servidor remoto.
c)Conexão com MongoDB: para enriquecer os dados, consultando informações como CPF, telefone, e outros dados complementares.
d)Análise e Higienização: limpeza de dados, remoção de duplicidades, normalização de colunas e mais.
e)Geração de Relatórios Profissionais (CSV, XLSX e PDF): com dashboards e análises prontas para uso.
f)Retorno do arquivo tratado ao sistema OwnCloud, tudo de forma assíncrona e automatizada.

## Conclusão:

O pyService funciona como um “cérebro de processamento” da aplicação, ele é a espinha dorsal de um sistema robusto. Ele automatiza 
toda a parte de higienização, enriquecimento e geração de relatórios, atuando como um serviço desacoplado que se comunica com:
i)RabbitMQ para comunicação assíncrona.
ii)MongoDB para enriquecimento de dados.
iii)OwnCloud para armazenamento e manipulação de arquivos.
iv)A API apenas intermedia, enquanto o pyService realiza todo o trabalho pesado.

Fluxo de Funcionamento Detalhado:

a) Recebe mensagens do RabbitMQ
i)Quando a API principal (em Node.js) detecta que há um novo arquivo no OwnCloud, ela envia uma mensagem para o RabbitMQ com os 
ii)metadados do arquivo (nome, caminho, tipo).
iii)O pyService está sempre escutando essa fila com um consumer.
iv)Assim que a mensagem chega, o serviço entra em ação e inicia o fluxo.

b) Baixa os arquivos do OwnCloud (work/)
i)O pyService acessa o OwnCloud via WebDAV (implementado em owncloud_utils.py) e baixa o arquivo localizado na pasta work/.
ii)O arquivo é salvo temporariamente na pasta storage/.

c) Higieniza e enriquece os dados (consulta o MongoDB)
Os dados do arquivo são lidos com Pandas.

A higienização ocorre linha por linha, aplicando:
i).strip() em colunas textuais.
ii)Remoção de colunas irrelevantes ou duplicadas.
iii)Normalização de dados inconsistentes.

Em seguida, o serviço realiza consultas no MongoDB:
i)Por exemplo: pega um CPF da planilha, busca na coleção nova_credlinks por dados como telefone, nome, etc.
ii)Esses dados são usados para preencher lacunas ou enriquecer colunas novas.

d) Gera relatórios e dashboards (CSV/XLSX e PDF)

Após o tratamento, o report_service.py entra em ação:
i)Cria um novo arquivo .csv ou .xlsx com os dados tratados.
ii)Gera um relatório visual em PDF com gráficos, totais, e estatísticas dos dados processados (ex: quantidade de CPFs únicos, 
erros, colunas incompletas, etc).
iii)Esses relatórios são armazenados em storage/temporário/.

e) Envia os arquivos processados para o OwnCloud (finalizado/)
i)O pyService pega todos os arquivos finais (planilha tratada + relatório PDF) e envia de volta para o OwnCloud.
ii)Eles são colocados na pasta finalizado/, sinalizando que o processo foi concluído com sucesso.


Diagrama do Fluxo com Detalhes:
Diagrama detalhado da arquitetura:

	  A[Usuário envia arquivo via API] --> 
A --> B[API envia mensagem para RabbitMQ]
B --> C[pyService escuta RabbitMQ]
C --> D[Baixa o arquivo do OwnCloud (work/)]
D --> E[Higieniza e enriquece os dados]
E --> F[Consulta dados no MongoDB (nova_credlinks)]
F --> G[Gera relatório (CSV/XLSX)]
G --> H[Cria PDF com análises e gráficos]
H --> I[Envia arquivos tratados para OwnCloud (finalizado/)]
I --> J[Notificação de sucesso para API]


Link do roadmap: https://roadmap.sh/r/pymicroservice 


1. Como Tudo se Conecta? (Explicação Detalhada)

a) A API recebe uma requisição POST /process com o nome do arquivo
Responsável: API principal (em Node.js)

i)Um cliente (usuário ou sistema externo) envia uma requisição HTTP para a API, solicitando o processamento de um determinado 
arquivo.
ii)Exemplo de payload:
{
  "fileName": "clientes-marco.csv"
}
iii)A API verifica se o arquivo está presente no OwnCloud (pasta work/) e se estiver tudo certo, avança para a próxima etapa.

b) O processFile envia a solicitação para o RabbitMQ
Responsável: A própria API, usando biblioteca como amqplib

i)A API se conecta ao RabbitMQ (fila file.process) e publica uma mensagem que inclui o nome do arquivo e, opcionalmente, o caminho 
e metadados.
ii)Exemplo da mensagem enviada:
{
  "file_name": "clientes-marco.csv",
  "path": "/storage/work/"
}
iii)Isso é feito por um módulo processFile (ou equivalente) que encapsula a lógica de envio de mensagens.

c) O pyService recebe a mensagem do RabbitMQ
Responsável: rabbitmq_consumer.py dentro do pyService

i)O pyService está escutando a fila file.process.
ii)Assim que uma nova mensagem é publicada, o consumer:
a)Lê o conteúdo.
b)Inicia o processamento, passando os dados da mensagem para os serviços responsáveis.
iii)A partir daqui, o fluxo de tratamento automático do arquivo começa.

d) O pyService baixa o arquivo do OwnCloud, higieniza, enriquece através do MongoDB e move para finalizado/
Responsáveis:
1)owncloud_utils.py: conexão e download/upload de arquivos.
2)file_service.py: higienização dos dados.
3)mongo_utils.py: enriquecimento de dados com base no MongoDB.
4)report_service.py: geração dos relatórios e dashboards.

Passo a passo interno:

i)Download: 
o arquivo é baixado da pasta work/ do OwnCloud.
ii)Higienização:
a)Remove espaços desnecessários, duplicações, caracteres especiais.
b)Normaliza nomes de colunas e formatação dos campos.
iii)Enriquecimento:
Com base em colunas como CPF ou email, o serviço busca dados no MongoDB (nova_credlinks) e adiciona novas colunas ao dataset.
iv)Geração de Relatórios:
a)Um novo arquivo .csv/.xlsx com os dados tratados é criado.
b)Um PDF com gráficos, totais e estatísticas é gerado.
v)Upload:
Todos os arquivos resultantes são enviados para o OwnCloud, na pasta finalizado/.

e) O RabbitMQ confirma que o arquivo foi processado:
Responsável: rabbitmq_consumer.py

i)Ao final de todo o fluxo, se não houver erros, o consumidor envia um ACK para o RabbitMQ, confirmando que a mensagem foi 
processada com sucesso.
ii)Se houver erro durante o processo:
a)A mensagem pode ser rejeitada (NACK) e reprocessada.
b)Pode ser redirecionada para uma Dead Letter Queue (DLQ), caso configurado.

f)Resumo Visual do Fluxo Completo:
sequenceDiagram
    participant Cliente
    participant API
    participant RabbitMQ
    participant pyService
    participant OwnCloud
    participant MongoDB

    Cliente  ->>API: POST /process { fileName }
    API      ->>RabbitMQ: Envia mensagem para fila file.process
    RabbitMQ ->>pyService: pyService consome a mensagem
    pyService->>OwnCloud: Baixa arquivo de work/
    pyService->>pyService: Higieniza e enriquece (Pandas + MongoDB)
    pyService->>MongoDB: Consulta dados (por CPF, e-mail, etc)
    pyService->>OwnCloud: Envia arquivos tratados para finalizado/
    pyService->>RabbitMQ: ACK (confirmação de processamento)


2. Dependências do pyService

# Dependências principais
pika==1.3.2                    # Conexão com RabbitMQ
pandas==2.1.4                  # Manipulação e análise de dados
pymongo==4.5.0                 # Conexão com MongoDB
matplotlib==3.8.0              # Geração de gráficos para relatórios
requests==2.31.0               # Requisições HTTP
owncloud==0.6                  # Integração com OwnCloud
openpyxl==3.1.2                # Manipulação de arquivos Excel
reportlab==4.0.4               # Geração de PDFs
python-dotenv==1.0.1           # Carregar variáveis de ambiente do .env
fpdf==1.7.2                    # Alternativa leve para gerar PDFs
pyocclient==0.5                # Cliente Python antigo para ownCloud

# Validações e configurações
pydantic==2.6.4                # Validação de dados com Python
pydantic-settings==2.2.1       # Configurações baseadas em Pydantic
pydantic-redis==0.1.1          # Integração entre Redis e Pydantic
pydantic-redis-settings==0.1.0 # Settings de Redis com Pydantic (experimental ou forkado)

# OBS: Pacotes como `pydantic-redis-settings` podem não estar disponíveis no PyPI oficial.
Confirme se são forks privados ou pacotes customizados.

# Apenas necessário se estiver usando Flask como API
flask==3.0.0
flask-cors==4.0.0
OBS: Se não for usar uma API HTTP no pyService, remova flask e flask-cors.
O pyService está rodando via RabbitMQ, então Flask e Flask-Cors só é necessário se for usada uma API HTTP.


3. Instalando e Executando o pyService

3.1 Rodando localmente
a)Instale as dependências na pasta do projeto: 
/mnt/c/users/cesar/pyService$ pip install -r requirements.txt
b)Inicie o consumidor do RabbitMQ: 
python src/routes/rabbitmq_consumer.py

Agora, sempre que a API enviar um arquivo para o RabbitMQ, o pyService irá:
i)Baixar o arquivo do OwnCloud
ii)Higienizar os dados e enriquecer com o MongoDB
iii)Gerar relatórios e gráficos
iv)Enviar o arquivo processado de volta para o OwnCloud

3.2 Rodando no Servidor
a)Atualize os pacotes e instale o Python: 
sudo apt update && sudo apt install -y python3 python3-pip
b)Instale as dependências manualmente: 
pip install pandas flask flask-cors pymongo pika openpyxl reportlab


4. Configuração do Docker:

4.1 docker-compose.yml
version: "3.8"

services:
  pyservice:
    build: .
    container_name: pyservice
    env_file: .env
    depends_on:
      redis:
        condition: service_healthy  # Espera até que o Redis esteja pronto
    restart: always
    networks:
      - pyservice_default
    volumes:
      - pyservice_data:/app/data  # Volume persistente para dados do pyservice
      - .:/app  # <<<<<< ISSO MONTA SEU CÓDIGO LOCAL TODO DENTRO DO CONTAINER
    extra_hosts:
      - "host.docker.internal:host-gateway"

  redis:
    image: "redis:latest"
    container_name: redis
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      retries: 5
      timeout: 3s
    networks:
      - pyservice_default

volumes:
  pyservice_data:
    # Define um volume chamado pyservice_data, usado para armazenar dados persistentes do pyservice.

networks:
  pyservice_default:
    external: true
    # Usa a rede externa pyservice_default para permitir a comunicação com RabbitMQ, MongoDB, etc.

4.2 Dockerfile
# Usa uma imagem leve do Python 3.9
FROM python:3.9-slim

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

4.3 Criando e Subindo os Containers
a)Execute:
i)docker network create pyservice_default  
	# Cria a rede necessária
ii)docker-compose down -v && docker-compose up --build -d
	# Isso remove volumes antigos, redes e containers e reconstrói tudo do zero.
b)Para verificar os logs:
docker logs -f pyservice


5. Funções e Responsabilidades

a)Arquivos de Configuração e Infraestrutura:
i)docker-compose.yml → Configuração dos serviços no Docker (RabbitMQ, MongoDB, OwnCloud e pyService).
ii)Dockerfile → Define a imagem do container para o pyService.
iii)requirements.txt → Lista de dependências do Python.
iv).env → Variáveis de ambiente para configuração.
v)main.py → Arquivo principal que inicializa o serviço.

b)Configuração e Conexões:
i) /src/config/settings.py → Configuração das variáveis de ambiente.
ii) /src/config/rabbitmq.py → Configuração da conexão com RabbitMQ (antes rabbitmqConfig.py).

c)Mensagens e Processamento no RabbitMQ:
/src/utils/rabbitmq.py → Envio e recebimento de mensagens no RabbitMQ (integrou rabbitmqRoutes.py).

d)Serviços e Processamento de Arquivos:
i) /src/services/rabbitmq_consumer.py → Consumidor do RabbitMQ que escuta a fila e encaminha mensagens para o processamento (antes 
estava em routes/).
ii) /src/controllers/rabbitmq_controller.py → Processa a mensagem recebida da fila e aciona os serviços de tratamento de arquivos.
iii) /src/services/file_service.py → Lógica de higienização e enriquecimento de dados.
iv) /src/services/report_service.py → Geração de relatórios PDF e dashboards.

e)Conexões com Outros Serviços:
i) /src/utils/owncloud.py → Conexão e manipulação de arquivos no OwnCloud.
ii) /src/utils/mongo.py → Conexão e consultas ao MongoDB.

f)Modelos de Dados:
/src/models/data_schema.py → Estrutura dos dados para enriquecimento.


6. Explicação dos Processos

6.1 Consumo de Mensagens do RabbitMQ

Objetivo: O pyService escuta mensagens do RabbitMQ para processar arquivos.

A fila "pyservice_queue" é utilizada para receber mensagens da API com os nomes dos arquivos.
O pyService fica escutando essa fila com BlockingConnection do pika.
Quando uma nova mensagem chega, o pyService busca o arquivo no OwnCloud e inicia o processamento.

Arquivo: rabbitmq_consumer.py

import pika
import json
from services.file_service import process_file

def callback(ch, method, properties, body):
    message = json.loads(body)
    file_name = message.get("file_name")
    process_file(file_name)

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="pyservice_queue")

channel.basic_consume(queue="pyservice_queue", on_message_callback=callback, auto_ack=True)
channel.start_consuming()

Conclusão:
i)O pyService automatiza a higienização e enriquecimento de dados.
ii)Ele integra RabbitMQ, MongoDB e OwnCloud para processamento eficiente.
iii)A API apenas encaminha os arquivos e o pyService faz o trabalho pesado.


# Estrutura do Projeto pyService

1. .dockerignore

Responsável por:
a)Definir quais arquivos e diretórios devem ser ignorados na hora de construir a imagem Docker.
b)Evita que arquivos desnecessários sejam enviados para o contexto da imagem.

Fluxo de execução:
Usado automaticamente pelo Docker durante o build da imagem.


2. .env

Responsável por:
Armazenar variáveis de ambiente sensíveis como URLs, credenciais e configurações.

Fluxo de execução:
Lido pelo settings.py para configurar a aplicação com base nas variáveis definidas.


3. .gitignore

Responsável por:
Informar ao Git quais arquivos ou diretórios não devem ser versionados (como .env, arquivos temporários, etc).

Fluxo de execução:
Lido automaticamente pelo Git durante operações de commit.


4. anotacoes_pyservice

Responsável por:
Contém anotações do desenvolvedor com ideias, rascunhos, fluxos de trabalho e observações.


5. docker-compose.yml

Responsável por:
Orquestrar a execução de containers (como pyService, RabbitMQ, MongoDB, etc).

Fluxo de execução:
a)Define os serviços necessários.
b)Permite subir tudo com docker-compose up.


6. Dockerfile

Responsável por:
Criar a imagem Docker do pyService.

a)Fluxo de execução:
b)Define base Python.
c)Copia arquivos.
d)Instala dependências do requirements.txt.
e)Define o comando de inicialização (CMD com main.py).


7. main.py

Responsável por:
a)Ponto de entrada da aplicação.
b)Inicializa o consumidor do RabbitMQ.

Fluxo de execução:
a)Carrega configurações (settings.py).
b)Inicia rabbitmq_consumer.py para escutar a fila.
c)Fica rodando em loop aguardando mensagens.


8. README.md

Responsável por:
Documentar o funcionamento do serviço, como rodar, dependências e estrutura.


9. requirements.txt

Responsável por:
Listar as dependências do projeto.

Fluxo de execução:
Usado no Dockerfile para instalar as bibliotecas com pip install -r requirements.txt.


10. /arquivos-para-consulta/

Responsável por:
Armazenar arquivos de referência, templates ou modelos para enriquecimento/higienização.


11. /storage/ (Diretório local de armazenamento usado pelo serviço)

11.1 work/

Responsável por:
Contém os arquivos CSV aguardando processamento.

11.2 finalizado/

Responsável por:
Armazena os arquivos já higienizados e enriquecidos.


12. /src/config/

12.1 rabbitmq_config.py

Responsável por:
Configurar host, porta, credenciais e nome da fila do RabbitMQ.

12.2 settings.py

Responsável por:
Carregar e fornecer acesso às variáveis de ambiente da aplicação (.env).

Fluxo de execução:
a)Usa dotenv para carregar variáveis.
b)Fornece constantes e configurações usadas globalmente.


13. /src/controllers/

13.1 rabbitmq_controller.py

Responsável por:
a)Controlar o processamento da mensagem recebida da fila.
b)Delegar o processamento aos serviços apropriados.

Fluxo de execução:
a)Recebe mensagem.
b)Extrai dados do arquivo.
c)Chama file_service e report_service.
d)Move arquivo para finalizado.


14. /src/models/

14.1 data_schema.py

Responsável por:
a)Definir estrutura dos dados esperados (ex: campos obrigatórios, CPF, telefone, etc).
b)Pode usar Pydantic ou dataclasses.


15. /src/routes/
Nota: Ainda está vazio. Pode ser usado futuramente caso o serviço receba requisições HTTP (Flask, FastAPI...).


16 /src/services/

16.1 file_service.py

Responsável por:
a)Higienização dos dados.
b)Enriquecimento via consultas ao MongoDB.
c)Salvar arquivo tratado em finalizado/.

Fluxo de execução:
a)Recebe o arquivo.
b)Higieniza linhas/colunas (ex: trim, remover duplicados).
c)Consulta MongoDB via mongo_utils.py.
d)Gera novo CSV.

16.2 rabbitmq_consumer.py

Responsável por:
a)Iniciar o consumo das mensagens do RabbitMQ.
b)Conectar com rabbitmq_controller.

Fluxo de execução:
a)Conecta na fila.
b)Fica ouvindo novas mensagens.
c)Ao receber, repassa para o controller.

16.3 report_service.py

Responsável por:
Gerar relatórios em PDF e dashboards a partir dos dados processados.

Fluxo de execução:
a)Recebe os dados higienizados.
b)Gera relatório visual em PDF com gráficos, tabelas, insights.


17. /src/tests/

17.1 send_test_message.py

Responsável por:
Enviar mensagens simuladas para a fila RabbitMQ (teste de integração).

Fluxo de execução:
a)Cria uma mensagem de teste (payload).
b)Usa rabbitmq_utils.py para enviar para a fila.


18 /src/utils/

18.1 rabbitmq_utils.py

Responsável por:
Funções auxiliares para enviar/receber mensagens no RabbitMQ.

Fluxo de execução:
Usado por consumer e send_test_message.

18.2 owncloud_utils.py

Responsável por:
a)Conexão com o OwnCloud Server.
b)Download dos arquivos do diretório work/.
c)Upload para finalizado/.

Fluxo de execução:
a)Conecta ao servidor.
b)Lê arquivos.
c)Envia arquivos processados.

Conclusão:
i)Utiliza o pacote owncloud para autenticação via WebDAV
ii)A pasta work/ armazena arquivos brutos
iii)A pasta finalizado/ armazena arquivos processados
iv)A comunicação acontece via owncloud_utils.py

18.3 mongo_utils.py

a)Responsável por:
b)Realizar queries no MongoDB.
c)Buscar dados para enriquecimento (ex: nome a partir do CPF, dados do telefone...).

Fluxo de execução:
a)Conecta no banco.
b)Executa consultas agregadas.
c)Retorna dados complementares para file_service.

Conclusão:
i)Utiliza pymongo para conexão e consultas no banco MongoDB
ii)Banco: uneel_unicomsi
iii)Coleção: nova_credlinks
iv)Usado para enriquecimento de dados com base em CPF e telefone
v)O enriquecimento é feito antes da geração de relatórios.

client = pymongo.MongoClient(MONGO_URL)
db = client["uneel_unicomsi"]
collection = db["nova_credlinks"]

Se o MongoDB estiver rodando fora do Docker, então seu MONGO_URI deve ser:
MONGO_URI=mongodb://host.docker.internal:27017
Isso funciona no Docker Desktop no Windows/macOS.

MONGO_URI=mongodb://host.docker.internal:27017
host.docker.internal é um alias padrão que o Docker Desktop fornece para acessar o host (o Windows ou o WSL2) de dentro de um 
container.


19. Integração com a API (Node.js)

A API envia tarefas ao RabbitMQ informando o nome do arquivo a ser processado. As rotas principais são:

a)fileProcessingRoutes.js
b)fileProcessingRoutesOwncloud.js
c)Essas rotas disparam eventos que são escutados pelo pyService, iniciando todo o fluxo descrito.

