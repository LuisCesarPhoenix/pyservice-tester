from src.services.file_service import process_csv
from src.utils.owncloud_utils import download_file, upload_file
from src.services.report_service import generate_pdf_report

def process_message(file_path):
    """Processa o arquivo recebido da fila"""
    try:
        print(f"[*] Processando arquivo: {file_path}")
        local_file = download_file(file_path)
        if not local_file:
            raise Exception("Falha ao baixar arquivo do OwnCloud")
            
        print(f"[*] Arquivo baixado com sucesso: {local_file}")
        processed_file = process_csv(local_file)
        if not processed_file:
            raise Exception("Falha ao processar arquivo CSV")

        report_pdf = processed_file.replace(".xlsx", ".pdf")
        if not generate_pdf_report(processed_file, report_pdf):
            raise Exception("Falha ao gerar relatório PDF")
            
        if not upload_file(report_pdf, report_pdf.split('/')[-1]):
            raise Exception("Falha ao fazer upload do relatório")
            
        print(f"[*] Arquivo processado com sucesso: {report_pdf}")
        return True
    except Exception as e:
        print(f"[!] Erro ao processar mensagem: {str(e)}")
        return False
