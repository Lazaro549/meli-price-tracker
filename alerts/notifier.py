import os
import smtplib
import requests
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()


def send_alert(title, item_id, current_price, min_price, drop_pct, currency, permalink):
    message = (
        f"🔔 Price drop alert!\n\n"
        f"Product : {title}\n"
        f"Previous min: {currency} {min_price:,.2f}\n"
        f"Current price: {currency} {current_price:,.2f}\n"
        f"Drop: -{drop_pct:.1f}%\n\n"
        f"🔗 {permalink}"
    )
    print(f"\n🔔 ALERT: {message}")
    _send_telegram(message)
    _send_email(title, message)


def _send_telegram(message: str):
    token   = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, json={"chat_id": chat_id, "text": message}, timeout=10)
        print("✅ Telegram alert sent.")
    except Exception as e:
        print(f"❌ Telegram error: {e}")


def _send_email(subject: str, body: str):
    sender   = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")
    if not all([sender, password, receiver]):
        return
    try:
        msg = MIMEText(body)
        msg["Subject"] = f"[MeliTracker] {subject}"
        msg["From"]    = sender
        msg["To"]      = receiver
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
        print("✅ Email alert sent.")
    except Exception as e:
        print(f"❌ Email error: {e}")
