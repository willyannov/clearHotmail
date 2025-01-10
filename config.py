import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém e valida as variáveis de ambiente
CLIENT_ID = os.getenv('CLIENT_ID')
TENANT_ID = os.getenv('TENANT_ID')
SCOPES = os.getenv('SCOPES')
TOKEN_FILE = os.getenv('TOKEN_FILE')

# Validação das variáveis obrigatórias
if not all([CLIENT_ID, TENANT_ID, SCOPES, TOKEN_FILE]):
    raise ValueError(
        "Variáveis de ambiente obrigatórias não encontradas. "
        "Certifique-se de que o arquivo .env existe e contém: "
        "CLIENT_ID, TENANT_ID, SCOPES, TOKEN_FILE"
    )

# Authentication URLs
DEVICE_CODE_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/devicecode"
TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token" 