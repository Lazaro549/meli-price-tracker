import requests


MELI_API = "https://api.mercadolibre.com/items/{}"


def fetch_item(item_id: str) -> dict | None:
    """Fetch price and title for a MeLi item_id (e.g. 'MLA1234567890')."""
    url = MELI_API.format(item_id)
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        return {
            "item_id": data["id"],
            "title":   data["title"],
            "price":   data["price"],
            "currency": data.get("currency_id", "ARS"),
            "permalink": data.get("permalink", ""),
        }
    except requests.RequestException as e:
        print(f"❌ Error fetching {item_id}: {e}")
        return None


def item_id_from_url(url: str) -> str | None:
    """Extract item_id from a Mercado Libre product URL."""
    import re
    match = re.search(r"(MLA-?\d+)", url, re.IGNORECASE)
    if match:
        return match.group(1).replace("-", "")
    return None
