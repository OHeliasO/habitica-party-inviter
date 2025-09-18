# Habitica Party Inviter

This project automates inviting users to a Habitica party using the Habitica API.

## Features
- Invite multiple users to a Habitica party
- Reads user data from a JSON file
- Uses environment variables for secure API authentication

### Invitation Limits

⚠️ **Important:** Habitica only allows **10 pending invites per party** at a time.  
This means our bot **cannot invite all users at once**—once the limit is reached, additional invites will be skipped until some pending invitations are accepted or expire.  

To avoid sending too many invites, the bot **only invites users who meet a minimum level requirement** (default: level equals or above 5). Users below this level will be automatically skipped.

## Requirements
- Python 3.11+
- Habitica account and API credentials

## Setup
1. Clone this repository:
   ```bash
   git clone <repo-url>
   cd habitica-party-inviter
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   # or, if using conda:
   conda env create -f environment.yml
   conda activate HABITICA
   ```
3. Copy the sample environment file and fill in your Habitica credentials:
   ```bash
   cp .env-sample .env
   # Edit .env with your API User ID and API Token
   ```

## Configuration
- Ensure your `.env` file contains the correct Habitica API credentials.

## Usage
Run the main script:
```bash
cd src
python main.py
```

## Notes
- Make sure your API credentials are kept secure and never shared publicly.
- Check the Habitica API documentation for more details: https://habitica.com/apidoc/

