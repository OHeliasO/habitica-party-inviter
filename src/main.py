import requests
import time
from config import API_USER_ID, API_TOKEN, API_GROUP_ID, API_CLIENT, CHECK_INTERVAL
from utils import load_invited_users, log_invite


LOOKING_FOR_PARTY_URL = "https://habitica.com/api/v4/looking-for-party"
INVITE_TO_PARTY_URL = f"https://habitica.com/api/v4/groups/{API_GROUP_ID}/invite"

headers = {
    "x-api-user": API_USER_ID,
    "x-api-key": API_TOKEN,
    "x-client": API_CLIENT,
    "Content-Type": "application/json"
}

def fetch_looking_users():
    resp = requests.get(LOOKING_FOR_PARTY_URL, headers=headers)    
    resp.raise_for_status()
    return resp.json().get("data", [])

def send_invite(user):
    """Invite a user to the group and log extended info."""
    user_id = user.get("_id")
    body = {"uuids": [user_id]}
    
    resp = requests.post(INVITE_TO_PARTY_URL, headers=headers, json=body)
    if resp.ok:
        print(f"✅ Invited {user.get('auth', {}).get('local', {}).get('username', user_id)} ({user_id})")
        log_invite(user)
    else:
        print(f"❌ Failed to invite {user.get('auth', {}).get('local', {}).get('username', user_id)} ({user_id}): {resp.status_code} - {resp.text}")


def main_loop():
    while True:
        try:
            invited = load_invited_users()
            users = fetch_looking_users()

            # example
            # Users: [{'_id': 'a id hahaha', 'auth': {'local': {'username': 'a suername'}, 'timestamps': {'created': '2025-09-18T11:39:37.503Z', 'loggedin': '2025-09-18T15:00:30.421Z', 'updated': '2025-09-18T15:02:45.519Z'}}, 'backer': {}, 'contributor': {}, 'flags': {'classSelected': False}, 'invited': False, 'items': {'gear': {'equipped': {'armor': 'armor_base_0', 'head': 'head_base_0', 'shield': 'shield_base_0', 'weapon': 'weapon_warrior_0'}, 'costume': {'armor': 'armor_base_0', 'head': 'head_base_0', 'shield': 'shield_base_0'}}}, 'loginIncentives': 1, 'preferences': {'hair': {'color': 'black', 'base': 1, 'bangs': 1, 'beard': 0, 'mustache': 0, 'flower': 1}, 'size': 'broad', 'skin': 'f5a76e', 'shirt': 'black', 'chair': 'none', 'language': 'ja', 'costume': False, 'background': 'violet'}, 'profile': {'name': 'a suername'}, 'stats': {'buffs': {'str': 0, 'int': 0, 'per': 0, 'con': 0, 'stealth': 0, 'streaks': False, 'seafoam': False, 'shinySeed': False, 'snowball': False, 'spookySparkles': False}, 'lvl': 1, 'class': 'warrior'}}]

            if users:
                print(f"👀 Found {len(users)} users looking for a party.")
                # print("Users:",users)

            for u in users:
                uid = u.get("_id")
                if not uid:
                    continue
                # We can only have 10 invites in waiting so we can't invite all users
                # **Check level before inviting**
                user_level = u.get("stats", {}).get("lvl", 0)
                if user_level < 5:
                    print(f"⏩ Skipping {uid}, level {user_level} is too low.")
                    continue

                if uid in invited:
                    print(f"⏩ Skipping {uid}, already invited before.")
                    continue
                send_invite(u)

        except Exception as e:
            print(f"⚠️ Error: {e}")

        print(f"⏳ Sleeping {CHECK_INTERVAL}s...")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main_loop()
