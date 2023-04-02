from dotenv import load_dotenv
load_dotenv()
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

CREDENCIAIS = {
'token': os.getenv("ACCESS_TOKEN"),
'refresh_token': os.getenv("REFRESH_TOKEN"),
'token_uri': 'https://oauth2.googleapis.com/token',
'client_id': os.getenv("CLIENT"),
'client_secret': os.getenv("CLIENT_SECRET"),
'scopes': ['https://www.googleapis.com/auth/drive.file']
}  

def fazer_upload_para_drive(nome_arquivo, caminho_arquivo, mimetype, id_pasta):
        # """Faz o upload de um arquivo para o Google Drive."""
        try:
            # Autentica com a API do Google Drive
            creds = Credentials.from_authorized_user_info(info=CREDENCIAIS)
            service = build('drive', 'v3', credentials=creds)
            novo_token = creds.refresh(Request())
            print(novo_token)

            # Cria o objeto MediaFileUpload com o arquivo a ser enviado
            media = MediaFileUpload(caminho_arquivo, mimetype=mimetype)

            # Faz o upload do arquivo para o Google Drive
            file_metadata = {'name': nome_arquivo, 'parents': [id_pasta]}
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

            # Retorna a URL do arquivo no Google Drive
            return f"https://drive.google.com/uc?export=view&id={file.get('id')}"
        except HttpError as error:
            print(f'Ocorreu um erro: {error}')
            return None