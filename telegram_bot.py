# telegram_bot.py

import requests
import time
from config import BOT_TOKEN, CHANNEL_ID, PERSONAL_CHAT_ID
from formatter import format_fixtures, format_match_result

def safe_send_request(url, payload, max_retries=5):
    for attempt in range(max_retries):
        try:
            r = requests.post(url, json=payload)
            if r.status_code == 200:
                print("✅ Message sent successfully.")
                return True
            else:
                print(f"❌ Telegram error: {r.text}")
        except Exception as e:
            print(f"❌ Failed to send Telegram message: {e}")
        if attempt < max_retries - 1:
            print("⏳ Retrying...")
            time.sleep(5)
    print("❌ Max retries reached. Failed to send the message.")
    return False

def send_message(text, chat_id=None, silent=False):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    max_length = 4096
    target_chat = chat_id or CHANNEL_ID

    parts = []
    while len(text) > max_length:
        idx = text.rfind('\n', 0, max_length)
        if idx == -1:
            idx = max_length
        parts.append(text[:idx].strip())
        text = text[idx:].strip()
    parts.append(text)

    for part in parts:
        payload = {
            "chat_id": target_chat,
            "text": part,
            "parse_mode": "Markdown",
            "disable_notification": silent
        }
        safe_send_request(url, payload)

def send_fixtures(matches):
    send_message(format_fixtures(matches))

def send_results(matches):
    for match in matches:
        send_message(format_match_result(match))

def send_keepalive():
    try:
        send_message(
            text="nigggga...🙈🙉",
            chat_id=PERSONAL_CHAT_ID,
            silent=True
        )
        print("⏲️ Sent keepalive heartbeat")
    except Exception as e:
        print(f"❌ Keepalive failed: {e}")
