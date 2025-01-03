# Outlook Email Manager

This project is an Outlook email manager that automatically moves emails classified as "other" to the trash using the Microsoft Graph API.

## Prerequisites

- Python 3.6 or higher
- Microsoft account with Outlook access
- Application registration in Azure Portal

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
   pip install (dependencies)
   ```

3. Configure the .env file:
   - Copy .env.example to .env
   ```bash
   cp .env.example .env
   ```
   - Edit the .env file with your credentials:
     - CLIENT_ID: Application ID obtained from Azure Portal
     - TENANT_ID: common (for personal accounts)
     - SCOPES: https://graph.microsoft.com/Mail.ReadWrite
     - TOKEN_FILE: outlook_token.json

4. Run the script:
   ```bash
   python outlook.py
   ```

5. On first run:
   - The script will generate an authentication code
   - Access the provided link
   - Log in with your Microsoft account
   - Enter the code shown in the terminal

## Features

- Automatic authentication with Microsoft Graph
- Access token caching to avoid repeated authentication
- Moves emails classified as "other" to trash
- Shows real-time progress
- Allows safe interruption with Ctrl+C

## Project Structure

```
.
├── outlook.py          # Main script
├── .env               # Sensitive settings (not versioned)
├── .env.example       # Configuration example
├── .gitignore         # Files ignored by git
└── README.md          # This file
```

## Security

- Never share your `.env` or `outlook_token.json` files
- Keep your CLIENT_ID secure
- The `.gitignore` file is already configured to exclude sensitive files

## Contributing

Feel free to contribute to the project through Pull Requests or by reporting issues.

## License

This project is under the MIT license. See the LICENSE file for more details.