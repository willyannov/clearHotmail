from dotenv import load_dotenv


import requests
import json
import os
from datetime import datetime, timedelta

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
TENANT_ID = os.getenv('TENANT_ID')
SCOPES = os.getenv('SCOPES')
TOKEN_FILE = os.getenv('TOKEN_FILE')

# URLs de autenticação
DEVICE_CODE_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/devicecode"
TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"

def save_token(token_data):
    token_data['expires_at'] = (datetime.now() + timedelta(seconds=token_data['expires_in'])).timestamp()
    with open(TOKEN_FILE, 'w') as f:
        json.dump(token_data, f)

def load_token():
    try:
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'r') as f:
                token_data = json.load(f)
                # Verifica se o token ainda é válido (com margem de 5 minutos)
                if datetime.now().timestamp() + 300 < token_data.get('expires_at', 0):
                    print("Token existente carregado com sucesso!")
                    return token_data.get('access_token')
    except Exception as e:
        print(f"Erro ao carregar token: {e}")
    return None

def get_access_token():
    token = load_token()
    if token:
        return token

    print("Obtendo novo token...")
    device_code_response = requests.post(
        DEVICE_CODE_URL,
        data={
            'client_id': CLIENT_ID,
            'scope': SCOPES
        }
    )
    
    if device_code_response.status_code != 200:
        print(f"Erro ao obter código de dispositivo: {device_code_response.text}")
        return None
    
    device_code_data = device_code_response.json()
    print(f"Acesse {device_code_data['verification_uri']} e insira o código: {device_code_data['user_code']}")
    
    while True:
        token_response = requests.post(
            TOKEN_URL,
            data={
                'client_id': CLIENT_ID,
                'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
                'device_code': device_code_data['device_code']
            }
        )
        
        token_data = token_response.json()
        
        if 'access_token' in token_data:
            print("Novo token obtido com sucesso!")
            save_token(token_data)  # Salva o token para uso futuro
            return token_data['access_token']
        
        if token_data.get('error') == 'authorization_pending':
            continue
        else:
            print(f"Erro durante a autenticação: {token_data.get('error_description')}")
            return None

# Exemplo de uso: Acessar os e-mails do Outlook
def get_emails(token):
    #url = "https://graph.microsoft.com/v1.0/me/messages"
    url = "https://graph.microsoft.com/v1.0/me/messages?$filter=inferenceClassification eq 'other'"
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        emails = response.json().get('value', [])
        for email in emails:
            
            print(f"Assunto: {email['subject']}")
            print(f"Remetente: {email['from']['emailAddress']['name']}")
            
    else:
        print(f"Erro ao buscar e-mails: {response.text}")
        

def move_to_trash(token):
    try:
        # URL específica para outros
        url = "https://graph.microsoft.com/v1.0/me/messages?$filter=inferenceClassification eq 'other'"
        headers = {
            'Authorization': f'Bearer {token}',
            'Prefer': 'outlook.allow-unsafe-html'
        }
        
        total_moved = 0
        next_link = url 
        
        while next_link:
            try:
                # Busca os emails da página atual
                response = requests.get(next_link, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    emails = data.get('value', [])
                    
                    for email in emails:
                        email_id = email['id']
                        sender = email['from']['emailAddress']['name']
                        subject = email['subject']
                        
                        
                        trash_url = f"https://graph.microsoft.com/v1.0/me/messages/{email_id}/move"
                        
                        # Mover para pasta "deletedItems" (lixeira)
                        move_response = requests.post(
                            trash_url,
                            headers=headers,
                            json={
                                "destinationId": "deletedItems"
                            }
                        )
                        
                        if move_response.status_code == 201:  # 201 = Created (sucesso)
                            print(f"Email movido para lixeira:")
                            print(f"De: {sender}")
                            print(f"Assunto: {subject}")
                            print("-" * 50)
                            total_moved += 1
                        else:
                            print(f"Erro ao mover email de {sender}: {move_response.text}")
                    
                    # Verifica se há mais páginas
                    next_link = data.get('@odata.nextLink')
                    if not next_link:
                        break
                else:
                    print(f"Erro ao buscar e-mails: {response.text}")
                    break
                    
            except KeyboardInterrupt:
                print("\nOperação interrompida pelo usuário!")
                print(f"Total de emails movidos até a interrupção: {total_moved}")
                return
            
        print(f"\nTotal de emails movidos para lixeira: {total_moved}")
            
    except KeyboardInterrupt:
        print("\nOperação interrompida pelo usuário!")
        print(f"Total de emails movidos até a interrupção: {total_moved}")
    except Exception as e:
        print(f"Erro durante a operação: {e}")
        print(f"Total de emails movidos até o erro: {total_moved}")

# Fluxo principal
if __name__ == "__main__":
    token = get_access_token()
    if token:
        #get_emails(token)
        move_to_trash(token)
