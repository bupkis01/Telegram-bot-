# config.py

import os
import base64
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN        = os.getenv("BOT_TOKEN")
CHANNEL_ID       = os.getenv("CHANNEL_ID")
GOOGLE_AI_KEY    = os.getenv("GOOGLE_AI_KEY")
PERSONAL_CHAT_ID = os.getenv("PERSONAL_CHAT_ID")

# Get and decode Base64-encoded Firebase key
FIREBASE_KEY_B64 = os.getenv("FIREBASE_KEY_B64")
if not FIREBASE_KEY_B64:
    raise ValueError("❌ Error: Missing FIREBASE_KEY_B64 in environment variables.")

# Ensure config/ exists, then write decoded JSON
os.makedirs("config", exist_ok=True)
key_json = base64.b64decode(FIREBASE_KEY_B64).decode("utf-8")
with open("config/firebase-key.json", "w") as f:
    f.write(key_json)

FIRESTORE_COLLECTION = "fixtures"
BASE_URL = "https://site.api.espn.com/apis/site/v2/sports/soccer"

# Validate critical env vars
if not all([BOT_TOKEN, CHANNEL_ID, GOOGLE_AI_KEY, PERSONAL_CHAT_ID]):
    raise ValueError("❌ Error: Missing one of BOT_TOKEN, CHANNEL_ID, GOOGLE_AI_KEY, or PERSONAL_CHAT_ID")

print("⚙️ Configuration loaded successfully.")
