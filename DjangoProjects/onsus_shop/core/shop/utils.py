import random
import string

import requests
from django.conf import settings


def generate_promo_code():
   letters = string.ascii_uppercase
   numbers = string.digits
   return ''.join(random.choices(letters + numbers, k=8))


def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }

    requests.post(url, data=data)


def send_telegram_photo(image_path, caption):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendPhoto"

    with open(image_path, "rb") as photo:
        files = {"photo": photo}
        data = {
            "chat_id": settings.TELEGRAM_CHAT_ID,
            "caption": caption,
            "parse_mode": "HTML"
        }

        response = requests.post(url, data=data, files=files, timeout=5)
        print(response.text)