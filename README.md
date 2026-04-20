# 📈 Meli Price Tracker
> Track Mercado Libre product prices over time and get notified when they drop.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-black?logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-embedded-blue?logo=sqlite)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-in%20development-orange)

---

## 🧠 What it does

- Fetches product prices from the **official Mercado Libre API** (no scraping)
- Stores historical price data in a local **SQLite** database
- Displays an interactive **price history chart** via a web dashboard
- Sends **alerts** (email or Telegram) when the price drops below a threshold

---

## 📸 Preview

> Dashboard screenshot coming soon.

---

## 🚀 Quickstart

### 1. Clone the repo

```bash
git clone https://github.com/Lazaro549/meli-price-tracker.git
cd meli-price-tracker
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

```bash
cp .env.example .env
# Edit .env with your config
```

### 4. Run the tracker

```bash
python tracker/scheduler.py
```

### 5. Open the dashboard

```bash
python dashboard/app.py
# Visit http://localhost:5000
```

---

## 🔑 How to get a product ID

From any Mercado Libre URL:

```
https://www.mercadolibre.com.ar/...MLA-1234567890...
                                      ↑
                                  This is the item_id
```

Use `MLA1234567890` (no dash) when adding a product to track.

---

## 📁 Project Structure

```
meli-price-tracker/
├── tracker/
│   ├── scraper.py        # Fetches price from MeLi API
│   ├── db.py             # SQLite read/write
│   └── scheduler.py      # Runs tracker every N hours
├── dashboard/
│   ├── app.py            # Flask web app
│   └── templates/
│       └── index.html    # Price history chart (Chart.js)
├── alerts/
│   └── notifier.py       # Email / Telegram notifications
├── .env.example
├── requirements.txt
└── README.md
```

---

## ⚙️ Configuration (`.env`)

```env
# Tracking interval in hours
INTERVAL_HOURS=6

# Alert threshold (percentage drop to trigger notification)
ALERT_THRESHOLD=5

# Telegram (optional)
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id

# Email (optional)
EMAIL_SENDER=you@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECEIVER=you@gmail.com
```

---

## 🗺️ Roadmap

- [x] Fetch price via MeLi public API
- [x] Store history in SQLite
- [x] Flask dashboard with Chart.js
- [ ] Multi-product tracking
- [ ] Compare sellers for the same product
- [ ] Detect "was/now" promotional discounts
- [ ] Docker + docker-compose support
- [ ] GitHub Actions for serverless scheduling
- [ ] PostgreSQL support for production deploys

---

## 🛠️ Tech Stack

| Layer      | Technology              |
|------------|-------------------------|
| Language   | Python 3.10+            |
| API        | Mercado Libre Items API |
| Database   | SQLite / PostgreSQL      |
| Scheduler  | APScheduler             |
| Dashboard  | Flask + Chart.js        |
| Alerts     | smtplib / Telegram Bot  |

---

## 🤝 Contributing

Pull requests are welcome! For major changes, open an issue first.

```bash
git checkout -b feature/your-feature
git commit -m "feat: your feature"
git push origin feature/your-feature
```

---

## 💸 Donations

If this project saved you time or money, consider supporting it:

| Currency | Alias |
|----------|-------|
| 🇦🇷 ARS (Argentina) | `lazaro.503.alaba.mp` |
| 🌎 USD (local transfers, Argentina only) | `ahogada.duras.foca` |

> Transfers via **Mercado Pago**.

---

## 📄 License

MIT © [Lazaro Gomez Vitolo](https://github.com/Lazaro549)
