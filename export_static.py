"""
Generates a fully static index.html from the SQLite DB.
Run after tracker/scheduler.py so data is fresh.
Output goes to ./docs/ (GitHub Pages source).
"""
import json
import os
from tracker.db import init_db, get_products, get_price_history

OUT_DIR = os.path.join(os.path.dirname(__file__), "docs")
os.makedirs(OUT_DIR, exist_ok=True)


def build_site():
    products = get_products()
    cards = []

    for p in products:
        history = get_price_history(p["item_id"])
        if not history:
            continue

        prices     = [h["price"] for h in history]
        timestamps = [h["timestamp"][:16] for h in history]  # trim seconds
        current    = prices[-1]
        minimum    = min(prices)
        currency   = history[-1]["currency"]
        drop       = round((minimum - current) / minimum * 100, 1) if minimum else 0

        cards.append({
            "item_id":   p["item_id"],
            "title":     p["title"],
            "url":       p["url"],
            "threshold": p["threshold"],
            "current":   current,
            "minimum":   minimum,
            "currency":  currency,
            "drop":      drop,
            "prices":    prices,
            "labels":    timestamps,
        })

    html = _render(cards)
    out  = os.path.join(OUT_DIR, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Static site generated → {out}")


def _render(cards: list) -> str:
    cards_html = ""
    for c in cards:
        color   = "#00a650" if c["drop"] < 0 else "#3483fa"
        arrow   = "↓" if c["drop"] < 0 else "→"
        data_js = json.dumps({"labels": c["labels"], "prices": c["prices"]})

        cards_html += f"""
        <div class="card">
          <h3><a href="{c['url']}" target="_blank">{c['title']}</a></h3>
          <div class="stats">
            <div><span>Current</span><strong>{c['currency']} {c['current']:,.0f}</strong></div>
            <div><span>Min ever</span><strong style="color:#00a650">{c['currency']} {c['minimum']:,.0f}</strong></div>
            <div><span>vs min</span><strong style="color:{color}">{arrow} {abs(c['drop'])}%</strong></div>
            <div><span>Alert at</span><strong>-{c['threshold']}%</strong></div>
          </div>
          <canvas id="chart-{c['item_id']}"></canvas>
          <script>
            (function() {{
              var d = {data_js};
              new Chart(document.getElementById("chart-{c['item_id']}"), {{
                type: "line",
                data: {{
                  labels: d.labels,
                  datasets: [{{ label: "Price", data: d.prices,
                    borderColor: "#3483fa", backgroundColor: "rgba(52,131,250,.08)",
                    fill: true, tension: 0.3, pointRadius: 2 }}]
                }},
                options: {{
                  plugins: {{ legend: {{ display: false }} }},
                  scales: {{
                    x: {{ ticks: {{ maxTicksLimit: 6, font: {{ size: 10 }} }} }},
                    y: {{ ticks: {{ font: {{ size: 10 }} }} }}
                  }}
                }}
              }});
            }})();
          </script>
        </div>"""

    updated = __import__("datetime").datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Meli Price Tracker</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:'Segoe UI',sans-serif;background:#f0f2f5;color:#333}}
    header{{background:#ffe600;padding:1rem 2rem;display:flex;align-items:center;justify-content:space-between}}
    header h1{{font-size:1.3rem}}
    header small{{font-size:.8rem;color:#555}}
    main{{max-width:860px;margin:2rem auto;padding:0 1rem}}
    .card{{background:#fff;border-radius:10px;padding:1.2rem 1.5rem;margin-bottom:1.2rem;box-shadow:0 1px 4px rgba(0,0,0,.1)}}
    .card h3{{margin-bottom:.3rem;font-size:1rem}}
    .card h3 a{{color:#3483fa;text-decoration:none}}
    .stats{{display:flex;gap:1.5rem;margin:.8rem 0;flex-wrap:wrap}}
    .stats div span{{font-size:.78rem;color:#888;display:block}}
    .stats div strong{{font-size:1.1rem}}
    canvas{{max-height:150px;width:100%!important}}
    .empty{{text-align:center;color:#aaa;padding:4rem}}
  </style>
</head>
<body>
  <header>
    <h1>📈 Meli Price Tracker</h1>
    <small>Updated: {updated}</small>
  </header>
  <main>
    {''.join(cards_html) if cards else '<div class="empty">No products tracked yet.</div>'}
  </main>
</body>
</html>"""


if __name__ == "__main__":
    init_db()
    build_site()
