import os
import time
from dotenv import load_dotenv
from tracker.db import init_db, get_products, save_price, get_min_price
from tracker.scraper import fetch_item
from alerts.notifier import send_alert

load_dotenv()

INTERVAL_HOURS = float(os.getenv("INTERVAL_HOURS", 6))
INTERVAL_SECS  = INTERVAL_HOURS * 3600


def run_once():
    products = get_products()
    if not products:
        print("⚠️  No products to track. Add one with add_product().")
        return

    for p in products:
        item_id   = p["item_id"]
        threshold = p["threshold"]

        data = fetch_item(item_id)
        if not data:
            continue

        price = data["price"]
        save_price(item_id, price, data["currency"])
        print(f"✅ {data['title'][:50]} → {data['currency']} {price:,.2f}")

        min_price = get_min_price(item_id)
        if min_price and price < min_price:
            drop_pct = (min_price - price) / min_price * 100
            if drop_pct >= threshold:
                send_alert(
                    title=data["title"],
                    item_id=item_id,
                    current_price=price,
                    min_price=min_price,
                    drop_pct=drop_pct,
                    currency=data["currency"],
                    permalink=data["permalink"],
                )


def run_loop():
    init_db()
    print(f"🚀 Tracker started. Interval: {INTERVAL_HOURS}h")
    while True:
        print("\n🔄 Checking prices...")
        run_once()
        print(f"⏳ Next check in {INTERVAL_HOURS}h")
        time.sleep(INTERVAL_SECS)


if __name__ == "__main__":
    run_loop()
