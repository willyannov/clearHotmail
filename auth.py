import requests
import json
import os
from datetime import datetime, timedelta
from config import CLIENT_ID, TENANT_ID, SCOPES, TOKEN_FILE, DEVICE_CODE_URL, TOKEN_URL

def save_token(token_data):
    token_data['expires_at'] = (datetime.now() + timedelta(seconds=token_data['expires_in'])).timestamp()
    with open(TOKEN_FILE, 'w') as f:
        json.dump(token_data, f)

def load_token():
    try:
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'r') as f:
                token_data = json.load(f)
                if datetime.now().timestamp() + 300 < token_data.get('expires_at', 0):
                    print("Existing token loaded successfully!")
                    return token_data.get('access_token')
    except Exception as e:
        print(f"Error loading token: {e}")
    return None

def get_access_token():
    token = load_token()
    if token:
        return token

    print("Getting new token...")
    device_code_response = requests.post(
        DEVICE_CODE_URL,
        data={
            'client_id': CLIENT_ID,
            'scope': SCOPES
        }
    )
    
    if device_code_response.status_code != 200:
        print(f"Error getting device code: {device_code_response.text}")
        return None
    
    device_code_data = device_code_response.json()
    print(f"Visit {device_code_data['verification_uri']} and enter the code: {device_code_data['user_code']}")
    
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
            print("New token obtained successfully!")
            save_token(token_data)
            return token_data['access_token']
        
        if token_data.get('error') == 'authorization_pending':
            continue
        else:
            print(f"Error during authentication: {token_data.get('error_description')}")
            return None 