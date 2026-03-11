import requests
from pathlib import Path

DATA_FOLDER = Path("data")

BULK_URL = "https://archives.nseindia.com/content/equities/bulk.csv"
BLOCK_URL = "https://archives.nseindia.com/content/equities/block.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}


def download_file(url, filename):

    try:
        response = requests.get(url, headers=HEADERS, timeout=20)

        if response.status_code == 200:

            filepath = DATA_FOLDER / filename

            with open(filepath, "wb") as f:
                f.write(response.content)

            print(f"Downloaded {filename}")

        else:
            print("Download failed:", response.status_code)

    except requests.exceptions.RequestException as e:
        print("Network error:", e)


def download_bulk_deals():
    download_file(BULK_URL, "bulk_deals.csv")


def download_block_deals():
    download_file(BLOCK_URL, "block_deals.csv")