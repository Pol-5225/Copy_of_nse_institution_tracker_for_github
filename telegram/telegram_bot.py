import requests


BOT_TOKEN = "8680341965:AAGAiVG9koLu8ZSOoMdYJ-YTQTyNdDOrABw"
CHAT_ID = "1470879004"


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