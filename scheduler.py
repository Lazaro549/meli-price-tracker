import os
import time
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler
from tracker.scraper import get_product
from tracker.db import init_db, save_price, get_min_price, get_tracked_items
from alerts.notifier import send_alert

load_dotenv()

INTERVAL_HOURS = int(os.getenv("INTERVAL_HOURS", 6))
ALERT_THRESHOLD = float(os.getenv("ALERT_THRESHOLD", 5))  # percent drop

# Add item IDs to track here
TRACKED_ITEMS = os.getenv("TRACKED_ITEMS", "").split(",")


def check_prices():
    items = [i.strip() for i in TRACKED_ITEMS if i.strip()]
    for item_id in items:
        try:
            product = get_product(item_id)
            min_price = get_min_price(item_id)
            save_price(item_id, product["title"], product["price"], product["currency"])
            print(f"[✓] {product['title']} → {product['currency']} {product['price']}")

            if min_price and product["price"] < min_price * (1 - ALERT_THRESHOLD / 100):
                send_alert(product)
        except Exception as e:
            print(f"[✗] Error tracking {item_id}: {e}")


if __name__ == "__main__":
    init_db()
    print(f"Tracker started. Checking every {INTERVAL_HOURS}h.")
    check_prices()  # Run immediately on start

    scheduler = BlockingScheduler()
    scheduler.add_job(check_prices, "interval", hours=INTERVAL_HOURS)
    scheduler.start()
