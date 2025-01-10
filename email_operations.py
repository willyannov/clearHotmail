import requests
import time
from filter_config import should_preserve_sender

def get_emails(token):
    try:
        # Adicionando parâmetros para melhor controle e ordenação
        url = "https://graph.microsoft.com/v1.0/me/messages?$top=1000&$orderby=receivedDateTime desc&$select=id,subject,from,receivedDateTime"
        headers = {
            'Authorization': f'Bearer {token}',
            'ConsistencyLevel': 'eventual'
        }
        
        total_checked = 0
        next_link = url
        
        print("\nListing emails... Press Ctrl+C at any time to stop.")
        
        while next_link:
            try:
                
                response = requests.get(next_link, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    emails = data.get('value', [])
                    
                    if not emails:
                        print("\nNo emails found!")
                        break
                    
                    for email in emails:
                        total_checked += 1
                        print("\n" + "=" * 50)
                        print(f"Email #{total_checked}")
                        print(f"Subject: {email['subject']}")
                        print(f"From: {email['from']['emailAddress']['name']} <{email['from']['emailAddress']['address']}>")
                        print(f"Date: {email['receivedDateTime']}")
                        print("=" * 50)
                    
                    next_link = data.get('@odata.nextLink')
                    if not next_link:
                        print(f"\nEnd of list. Total emails: {total_checked}")
                        break
                        
                    if input("\nPress ENTER to continue listing or 'q' to quit: ").lower() == 'q':
                        print(f"\nListing interrupted. Total emails listed: {total_checked}")
                        break
                        
                elif response.status_code == 401:
                    print("\nToken expired or invalid. Please renew your access token.")
                    break
                elif response.status_code == 429:
                    print("\nToo many requests. Waiting before trying again...")
                    time.sleep(5)  # Espera 30 segundos antes de tentar novamente
                    continue
                else:
                    error_data = response.json().get('error', {})
                    error_message = error_data.get('message', 'Unknown error')
                    error_code = error_data.get('code', 'Unknown code')
                    print(f"\nError fetching emails: {error_code} - {error_message}")
                    break
                    
            except KeyboardInterrupt:
                print(f"\n\nOperation interrupted! Total emails listed: {total_checked}")
                return
            except Exception as e:
                print(f"\nError processing email page: {e}")
                break
                
    except Exception as e:
        print(f"\nError during operation: {e}")

def move_to_trash(token):
    try:
        # Adicionando parâmetros para melhor controle e ordenação
        url = "https://graph.microsoft.com/v1.0/me/messages?$top=50&$orderby=receivedDateTime desc&$select=id,subject,from,receivedDateTime"
        headers = {
            'Authorization': f'Bearer {token}',
            'Prefer': 'outlook.allow-unsafe-html',
            'ConsistencyLevel': 'eventual'
        }
        
        total_moved = 0
        total_preserved = 0
        next_link = url 
        
        while next_link:
            try:
                # Adicionando um pequeno delay entre as requisições
                
                response = requests.get(next_link, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    emails = data.get('value', [])
                    
                    for email in emails:
                        email_id = email['id']
                        sender = email['from']['emailAddress']['name']
                        subject = email['subject']
                        
                        # Verifica se o remetente deve ser preservado
                        if should_preserve_sender(sender):
                            print(f"Email preserved (sender in whitelist):")
                            print(f"From: {sender}")
                            print(f"Subject: {subject}")
                            print("-" * 50)
                            total_preserved += 1
                            continue
                   
                        
                        trash_url = f"https://graph.microsoft.com/v1.0/me/messages/{email_id}/move"
                        
                        move_response = requests.post(
                            trash_url,
                            headers=headers,
                            json={
                                "destinationId": "deletedItems"
                            }
                        )
                        
                        if move_response.status_code == 201:
                            print(f"Email moved to trash:")
                            print(f"From: {sender}")
                            print(f"Subject: {subject}")
                            print("-" * 50)
                            total_moved += 1
                        elif move_response.status_code == 429:
                            print("\nToo many requests. Waiting before trying again...")
                            time.sleep(5)  # Espera 30 segundos antes de tentar novamente
                            continue
                        else:
                            error_data = move_response.json().get('error', {})
                            error_message = error_data.get('message', 'Unknown error')
                            error_code = error_data.get('code', 'Unknown code')
                            print(f"Error moving email from {sender}: {error_code} - {error_message}")
                    
                    next_link = data.get('@odata.nextLink')
                    if not next_link:
                        break
                elif response.status_code == 401:
                    print("\nToken expired or invalid. Please renew your access token.")
                    break
                elif response.status_code == 429:
                    print("\nToo many requests. Waiting before trying again...")
                    time.sleep(5)  # Espera 30 segundos antes de tentar novamente
                    continue
                else:
                    error_data = response.json().get('error', {})
                    error_message = error_data.get('message', 'Unknown error')
                    error_code = error_data.get('code', 'Unknown code')
                    print(f"Error fetching emails: {error_code} - {error_message}")
                    break
                    
            except KeyboardInterrupt:
                print("\nOperation interrupted by user!")
                print(f"Total emails moved until interruption: {total_moved}")
                print(f"Total emails preserved: {total_preserved}")
                return
            
        print(f"\nTotal emails moved to trash: {total_moved}")
        print(f"Total emails preserved: {total_preserved}")
            
    except KeyboardInterrupt:
        print("\nOperation interrupted by user!")
        print(f"Total emails moved until interruption: {total_moved}")
        print(f"Total emails preserved: {total_preserved}")
    except Exception as e:
        print(f"Error during operation: {e}")
        print(f"Total emails moved until error: {total_moved}")
        print(f"Total emails preserved: {total_preserved}") 