import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, ENABLE_TELEGRAM, ENABLE_SOUND

def notify(text: str, enable_sound: bool = False):
    print(text)
    if enable_sound or ENABLE_SOUND:
        print("\a")

def send_telegram_message(text: str):
    if not ENABLE_TELEGRAM:
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    print(payload)
    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
        print("[Telegram] Sent")
    except Exception as e:
        print(f"[Telegram] Send failed: {e}")