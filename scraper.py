import requests

MELI_API = "https://api.mercadolibre.com/items"


def get_product(item_id: str) -> dict:
    """Fetch product data from MeLi public API."""
    response = requests.get(f"{MELI_API}/{item_id}", timeout=10)
    response.raise_for_status()
    data = response.json()
    return {
        "item_id": data["id"],
        "title": data["title"],
        "price": data["price"],
        "currency": data["currency_id"],
        "condition": data["condition"],
        "permalink": data["permalink"],
    }
