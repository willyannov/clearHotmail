# Outlook Email Manager

This project is an Outlook email manager that automatically moves emails classified as "other" to the trash using the Microsoft Graph API.

## Prerequisites

- Python 3.6 or higher
- Microsoft account with Outlook access
- Application registration in Azure Portal
- Required Python packages:
  - requests
  - python-dotenv
  - time

## Azure Configuration

1. Access [Azure Portal](https://portal.azure.com)
2. Register a new application:
   - Go to "Azure Active Directory" > "App registrations"
   - Click on "New registration"
   - Give your application a name
   - Under "Supported account types", select "Accounts in any organizational directory and personal Microsoft accounts"
   - Click "Register"
3. After registration, copy the "Application (client) ID" - you'll need it for the `.env` file

4. Configure API permissions:
   - In Azure Portal, go to your application registration
   - Click on "API permissions"
   - Click "Add a permission"
   - Select "Microsoft Graph"
   - Choose "Delegated permissions"
   - Search and select the following permissions:
     - Mail.ReadWrite (Read and write mail)
     - Mail.Send (Send mail)
     - User.Read (Read basic user profile)
   - Click "Add permissions"
   - Click "Grant admin consent" (if needed)

5. Configure authentication:
   - In the side menu, click "Authentication"
   - Under "Platform configurations", click "Add a platform"
   - Select "Mobile and desktop applications"
   - Check "https://login.microsoftonline.com/common/oauth2/nativeclient"
   - Save the changes

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/willyannov/clearHotmail.git
   cd clearHotmail
   ```

2. Install dependencies:
   ```bash
   pip install requests python-dotenv
   ```

3. Configure the .env file:
   - Copy .env.example to .env
   ```bash
   cp .env.example .env
   ```
   - Edit the .env file with your credentials:
     ```
     CLIENT_ID=your_client_id_here
     TENANT_ID=common
     SCOPES=https://graph.microsoft.com/Mail.ReadWrite
     TOKEN_FILE=outlook_token.json
     ```

4. Configure email filters (optional):
   - Edit `filter_config.py` to add or remove email senders that should not be moved to trash
   - The default list includes common job sites and development platforms
   - Add new senders following the existing format:
     ```python
     PRESERVED_SENDERS = [
         'LinkedIn',
         'GitHub',
         # Add more senders here
     ]
     ```

5. Run the script:
   ```bash
   python outlook.py
   ```

6. On first run:
   - The script will generate an authentication code
   - Access the provided link
   - Log in with your Microsoft account
   - Enter the code shown in the terminal

## Features

- Automatic authentication with Microsoft Graph
- Access token caching to avoid repeated authentication
- Moves emails to trash with configurable filters
- Email sender whitelist to preserve important messages
- Shows real-time progress with detailed information
- Rate limiting protection with automatic retry
- Allows safe interruption with Ctrl+C
- Supports pagination for large email lists

## Project Structure

```
.
├── outlook.py          # Main script with menu interface
├── email_operations.py # Email handling operations
├── auth.py            # Authentication functions
├── config.py          # Configuration and environment setup
├── filter_config.py   # Email filter settings
├── .env               # Sensitive settings (not versioned)
├── .env.example       # Configuration example
├── .gitignore         # Files ignored by git
└── README.md          # This file
```

## Security

- Never share your `.env` or `outlook_token.json` files
- Keep your CLIENT_ID secure
- The `.gitignore` file is already configured to exclude sensitive files
- Token is automatically refreshed when expired

Feel free to contribute to the project through Pull Requests or by reporting issues.
