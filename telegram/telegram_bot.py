import os
import requests
import time   # <-- added for delay

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHAT_IDS = [
    os.getenv("CHAT_ID"),        # your personal chat
    os.getenv("GROUP_CHAT_ID")   # telegram group
]

# Safety check
if not BOT_TOKEN:
    print("⚠ Telegram BOT_TOKEN missing.")

def send_message(message):
    print("BOT_TOKEN loaded:", bool(BOT_TOKEN))
    print("CHAT_IDS loaded:", CHAT_IDS)

    if not BOT_TOKEN:
        raise RuntimeError("Missing BOT_TOKEN environment variable")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    for chat_id in CHAT_IDS:

        if not chat_id:
            continue

        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }

        resp = requests.post(url, data=payload, timeout=20)

        print("Sending to:", chat_id)
        print("Telegram API status:", resp.status_code)
        print("Telegram API response:", resp.text)

        data = resp.json()
        if not data.get("ok"):
            raise RuntimeError(f"Telegram error: {data}")

        # 🔹 Prevent Telegram rate limit (429 error)
        time.sleep(1)

    return True


if __name__ == "__main__":
    send_message("Test message from NSE institutional tracker 🚀")