import os
import owncloud
import requests
from requests.auth import HTTPBasicAuth
from src.config.settings import OWNCLOUD_URL, OWNCLOUD_USER, OWNCLOUD_PASS, REMOTE_WORK_DIR, WORK_DIR, FINALIZED_DIR

def connect_owncloud():
    print(WORK_DIR)
    """Conecta ao servidor OwnCloud"""
    try:
        # Use the older WebDAV endpoint format
        base_url = OWNCLOUD_URL + '/remote.php/webdav/'
        print(f"[*] Conectando ao OwnCloud: {base_url}")
        
        # Criar uma sessão com autenticação básica
        session = requests.Session()
        session.auth = HTTPBasicAuth(OWNCLOUD_USER, OWNCLOUD_PASS)
        session.verify = False
        
        # Teste de conexão
        response = session.request('PROPFIND', base_url)
        if response.status_code in (401, 403):
            raise Exception(f"Falha na autenticação: {response.status_code}")
            
        # Se chegou aqui, a autenticação funcionou
        oc = owncloud.Client(base_url)
        oc._session = session  # Usar a sessão já autenticada
        print("[*] Conectado com sucesso ao OwnCloud")
        return oc
            
    except Exception as e:
        print(f"[!] Erro ao conectar ao OwnCloud: {str(e)}")
        return None

def download_file(file_path):
    """Download do arquivo do OwnCloud"""
    try:
        oc = connect_owncloud()
        if not oc:
            raise Exception("Falha na conexão com OwnCloud")
        remote_path = f"/{REMOTE_WORK_DIR}/{file_path}"
        print(f"[*] Baixando arquivo {remote_path}")
        local_path = f"{WORK_DIR}/{file_path}"
        print(f"[*] Baixando arquivo {remote_path} para {local_path}")
        
        # Fazer o download usando a sessão diretamente
        url = f"{OWNCLOUD_URL.rstrip('/')}/remote.php/dav/files/uneel_adm{remote_path}"
        print(f"[*] URL de download: {url}")
        response = oc._session.get(url)
        
        if response.status_code == 200:
            # Criar diretórios se necessário
            import os
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            # Salvar o arquivo
            with open(local_path, 'wb') as f:
                f.write(response.content)
            return local_path
        else:
            raise Exception(f"Erro ao baixar arquivo: {response.status_code}")
            
    except Exception as e:
        print(f"[!] Erro ao baixar arquivo {file_path}: {str(e)}")
        return None

def upload_file(local_path, remote_path):
    """Upload do arquivo para o OwnCloud"""
    try:
        oc = connect_owncloud()
        if not oc:
            raise Exception("Falha na conexão com OwnCloud")
            
        remote_path = f"{FINALIZED_DIR}{remote_path}"
        print(f"[*] Fazendo upload de {local_path} para {remote_path}")
        
        # Fazer o upload usando a sessão diretamente
        url = f"{OWNCLOUD_URL.rstrip('/')}/remote.php/webdav/{remote_path}"
        with open(local_path, 'rb') as f:
            response = oc._session.put(url, data=f)
            
        if response.status_code not in (200, 201, 204):
            raise Exception(f"Erro ao fazer upload: {response.status_code}")
        return True
            
    except Exception as e:
        print(f"[!] Erro ao fazer upload do arquivo {local_path}: {str(e)}")
        return False
