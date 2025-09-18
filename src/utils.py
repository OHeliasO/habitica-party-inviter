import json
import os
from datetime import datetime
from config import INVITED_FILE  # e.g., "invited_users.json"

def load_invited_users():
    """Load invited users from JSON log file into a set (by user_id)."""
    if os.path.exists(INVITED_FILE):
        with open(INVITED_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []
    # Return a set of IDs for quick lookup
    return set(user["user_id"] for user in data)

def log_invite(user):
    """Log a newly invited user to the JSON file."""
    user_id = user.get("_id")
    username = user.get("auth", {}).get("local", {}).get("username", "unknown")
    level = user.get("stats", {}).get("lvl", 0)
    login_count = user.get("loginIncentives", 0)  # or len(auth.timestamps) if you track multiple logins
    invited_at = datetime.utcnow().isoformat()

    # Load existing data
    if os.path.exists(INVITED_FILE):
        with open(INVITED_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # Append new user
    data.append({
        "user_id": user_id,
        "username": username,
        "level": level,
        "login_count": login_count,
        "invited_at": invited_at
    })

    # Write back
    with open(INVITED_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)