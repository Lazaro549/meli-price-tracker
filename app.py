from flask import Flask, render_template, request, jsonify
from tracker.db import init_db, get_history, get_tracked_items, save_price
from tracker.scraper import get_product

app = Flask(__name__)
init_db()


@app.route("/")
def index():
    items = get_tracked_items()
    return render_template("index.html", items=items)


@app.route("/api/history/<item_id>")
def history(item_id):
    return jsonify(get_history(item_id))


@app.route("/api/add", methods=["POST"])
def add_item():
    item_id = request.json.get("item_id", "").strip().upper()
    try:
        product = get_product(item_id)
        save_price(item_id, product["title"], product["price"], product["currency"])
        return jsonify({"ok": True, "title": product["title"]})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
