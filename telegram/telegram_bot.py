import os
import requests

# Read values from GitHub secrets (environment variables)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_message(message):
    """
    Send message to Telegram
    """

    print("BOT_TOKEN loaded:", BOT_TOKEN is not None)
    print("CHAT_ID loaded:", CHAT_ID is not None)

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=payload)

    print("Telegram API response:")
    print(response.text)

    return response.json()


if __name__ == "__main__":
    send_message("Test message from NSE institutional tracker 🚀")