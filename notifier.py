import os
import smtplib
import requests
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()


def send_telegram(message: str):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": message})


def send_email(subject: str, body: str):
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")
    if not all([sender, password, receiver]):
        return
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)


def send_alert(product: dict):
    message = (
        f"💸 Price drop alert!\n"
        f"{product['title']}\n"
        f"New price: {product['currency']} {product['price']}\n"
        f"{product['permalink']}"
    )
    print(f"[ALERT] {message}")
    send_telegram(message)
    send_email("💸 Price Drop - Meli Tracker", message)
