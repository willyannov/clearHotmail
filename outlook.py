import requests
import json
import os
from datetime import datetime, timedelta

CLIENT_ID = os.getenv('CLIENT_ID')
TENANT_ID = os.getenv('TENANT_ID')
SCOPES = os.getenv('SCOPES')
TOKEN_FILE = os.getenv('TOKEN_FILE')

# Authentication URLs
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
                # Check if token is still valid (with 5 minutes margin)
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
            save_token(token_data)  # Save token for future use
            return token_data['access_token']
        
        if token_data.get('error') == 'authorization_pending':
            continue
        else:
            print(f"Error during authentication: {token_data.get('error_description')}")
            return None

def get_emails(token):
    url = "https://graph.microsoft.com/v1.0/me/messages?$filter=inferenceClassification eq 'other'"
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        emails = response.json().get('value', [])
        for email in emails:
            print(f"Subject: {email['subject']}")
            print(f"From: {email['from']['emailAddress']['name']}")
    else:
        print(f"Error fetching emails: {response.text}")

def move_to_trash(token):
    try:
        # URL specific for others
        url = "https://graph.microsoft.com/v1.0/me/messages?$filter=inferenceClassification eq 'other'"
        headers = {
            'Authorization': f'Bearer {token}',
            'Prefer': 'outlook.allow-unsafe-html'
        }
        
        total_moved = 0
        next_link = url 
        
        while next_link:
            try:
                # Fetch emails from current page
                response = requests.get(next_link, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    emails = data.get('value', [])
                    
                    for email in emails:
                        email_id = email['id']
                        sender = email['from']['emailAddress']['name']
                        subject = email['subject']
                        
                        trash_url = f"https://graph.microsoft.com/v1.0/me/messages/{email_id}/move"
                        
                        # Move to "deletedItems" folder (trash)
                        move_response = requests.post(
                            trash_url,
                            headers=headers,
                            json={
                                "destinationId": "deletedItems"
                            }
                        )
                        
                        if move_response.status_code == 201:  # 201 = Created (success)
                            print(f"Email moved to trash:")
                            print(f"From: {sender}")
                            print(f"Subject: {subject}")
                            print("-" * 50)
                            total_moved += 1
                        else:
                            print(f"Error moving email from {sender}: {move_response.text}")
                    
                    # Check if there are more pages
                    next_link = data.get('@odata.nextLink')
                    if not next_link:
                        break
                else:
                    print(f"Error fetching emails: {response.text}")
                    break
                    
            except KeyboardInterrupt:
                print("\nOperation interrupted by user!")
                print(f"Total emails moved until interruption: {total_moved}")
                return
            
        print(f"\nTotal emails moved to trash: {total_moved}")
            
    except KeyboardInterrupt:
        print("\nOperation interrupted by user!")
        print(f"Total emails moved until interruption: {total_moved}")
    except Exception as e:
        print(f"Error during operation: {e}")
        print(f"Total emails moved until error: {total_moved}")

# Main flow
if __name__ == "__main__":
    token = get_access_token()
    if token:
        move_to_trash(token)
