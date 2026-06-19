import os

DATA_DIR = "data"

os.makedirs(DATA_DIR, exist_ok=True)

DEFAULT_HEADERS = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        " AppleWebKit/537.36 (KHTML, like Gecko)"
        " Chrome/131.0.0.0 Safari/537.36",

    "Accept":
        "application/json, text/javascript, */*; q=0.01",

    "X-Requested-With":
        "XMLHttpRequest"
}