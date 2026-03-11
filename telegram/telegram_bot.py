import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Safety check
if not BOT_TOKEN or not CHAT_ID:
    print("⚠ Telegram credentials missing. BOT_TOKEN or CHAT_ID not found.")

def send_message(message):
    print("BOT_TOKEN loaded:", bool(BOT_TOKEN))
    print("CHAT_ID loaded:", bool(CHAT_ID))

    if not BOT_TOKEN or not CHAT_ID:
        raise RuntimeError("Missing BOT_TOKEN or CHAT_ID environment variable")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    resp = requests.post(url, data=payload, timeout=20)
    print("Telegram API status:", resp.status_code)
    print("Telegram API response:", resp.text)

    data = resp.json()
    if not data.get("ok"):
        raise RuntimeError(f"Telegram error: {data}")

    return data

if __name__ == "__main__":
    send_message("Test message from NSE institutional tracker 🚀")