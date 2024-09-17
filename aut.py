from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Configurações
SERVICE_ACCOUNT_FILE = 'path/to/your/service_account.json'  # Caminho para o arquivo de credenciais JSON
SCOPES = ['https://www.googleapis.com/auth/drive']

# Autenticação
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=creds)

# Função para fazer upload do arquivo
def upload_file(file_path, mime_type):
    file_metadata = {'name': file_path.split('/')[-1]}  # Nome do arquivo
    media = MediaFileUpload(file_path, mimetype=mime_type)
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    return file.get('id')

# Função para compartilhar o arquivo com um colaborador
def share_file(file_id, email, role='reader'):
    service.permissions().create(
        fileId=file_id,
        body={
            'role': role,  # 'reader' ou 'writer'
            'type': 'user',
            'emailAddress': email
        },
        fields='id'
    ).execute()

# Função para processar arquivos e colaboradores
def process_files_and_collaborators(file_collaborator_map):
    for file_path, email in file_collaborator_map.items():
        print(f"Uploading file {file_path} for {email}...")
        file_id = upload_file(file_path, 'application/octet-stream')
        print(f"Sharing file with ID {file_id} to {email}...")
        share_file(file_id, email)

# Exemplo de uso
file_collaborator_map = {
    'path/to/your/file1.txt': 'collaborator1@example.com',
    'path/to/your/file2.txt': 'collaborator2@example.com',
    'path/to/your/file3.txt': 'collaborator3@example.com'
}

process_files_and_collaborators(file_collaborator_map)
