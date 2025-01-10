from auth import get_access_token
from email_operations import move_to_trash, get_emails
import sys
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu():
    clear_screen()
    print("\n=== Outlook Email Manager ===")
    print("1. Get/Renew Access Token")
    print("2. List Emails")
    print("3. Move Emails to Trash")
    print("4. Exit")
    print("=" * 28)

def handle_token():
    try:
        token = get_access_token()
        if token:
            print("\nToken obtained successfully!")
        else:
            print("\nUnable to obtain access token.")
        input("\nPress ENTER to continue...")
        return token
    except Exception as e:
        print(f"\nError getting token: {e}")
        input("\nPress ENTER to continue...")
        return None

def handle_trash(token):
    if not token:
        print("\nToken not found. Please obtain a token first.")
        input("\nPress ENTER to continue...")
        return
    
    try:
        move_to_trash(token)
        input("\nPress ENTER to continue...")
    except Exception as e:
        print(f"\nError moving emails: {e}")
        input("\nPress ENTER to continue...")

def handle_list_emails(token):
    if not token:
        print("\nToken not found. Please obtain a token first.")
        input("\nPress ENTER to continue...")
        return
    
    try:
        get_emails(token)
        input("\nPress ENTER to continue...")
    except Exception as e:
        print(f"\nError listing emails: {e}")
        input("\nPress ENTER to continue...")

def main():
    token = None
    while True:
        try:
            show_menu()
            option = input("\nChoose an option (1-4): ")

            if option == "1":
                token = handle_token()
            elif option == "2":
                handle_list_emails(token)  
            elif option == "3":
                handle_trash(token)
            elif option == "4":
                print("\nExiting program...")
                sys.exit(0)
            else:
                print("\nInvalid option!")
                input("\nPress ENTER to continue...")

        except KeyboardInterrupt:
            print("\n\nOperation interrupted by user.")
            sys.exit(0)
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            input("\nPress ENTER to continue...")

if __name__ == "__main__":
    main()
