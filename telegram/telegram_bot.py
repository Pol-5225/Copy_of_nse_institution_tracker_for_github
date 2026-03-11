import requests


BOT_TOKEN = "BOT_TOKEN"
CHAT_ID = "CHAT_ID"


def send_message(message):
    """
    Send message to Telegram
    """

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=payload)

    return response.json()

if __name__ == "__main__":
    send_message("Test message from NSE institutional tracker 🚀")