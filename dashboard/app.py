from flask import Flask, render_template, request, redirect, url_for
from tracker.db import init_db, get_products, get_price_history, add_product
from tracker.scraper import fetch_item, item_id_from_url
import os

app = Flask(__name__)


@app.route("/")
def index():
    products = get_products()
    data = []
    for p in products:
        history = get_price_history(p["item_id"])
        current = history[-1]["price"] if history else None
        minimum = min(h["price"] for h in history) if history else None
        data.append({**p, "current": current, "minimum": minimum, "history": history})
    return render_template("index.html", products=data)


@app.route("/add", methods=["POST"])
def add():
    raw       = request.form.get("url_or_id", "").strip()
    threshold = float(request.form.get("threshold", 5.0))

    item_id = item_id_from_url(raw) if raw.startswith("http") else raw.upper()
    if not item_id:
        return "Invalid URL or item ID", 400

    item = fetch_item(item_id)
    if not item:
        return "Could not fetch item from MeLi API", 400

    add_product(item_id, item["title"], item["permalink"], threshold)
    return redirect(url_for("index"))


@app.route("/product/<item_id>")
def product(item_id):
    history = get_price_history(item_id)
    products = get_products()
    info = next((p for p in products if p["item_id"] == item_id), None)
    return render_template("product.html", info=info, history=history)


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
