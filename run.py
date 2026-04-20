"""
run.py — Entry point for Meli Price Tracker.

Usage:
    python run.py            # starts both dashboard + tracker
    python run.py --web      # dashboard only
    python run.py --tracker  # tracker only
"""

import sys
import threading
from tracker.db import init_db
from tracker.scheduler import run_loop
from dashboard.app import app


def start_tracker():
    run_loop()


def start_dashboard():
    app.run(debug=False, port=5000, use_reloader=False)


if __name__ == "__main__":
    init_db()

    mode = sys.argv[1] if len(sys.argv) > 1 else "--both"

    if mode == "--web":
        print("🌐 Starting dashboard on http://localhost:5000")
        start_dashboard()

    elif mode == "--tracker":
        print("🔄 Starting tracker only")
        start_tracker()

    else:
        print("🚀 Starting dashboard + tracker")
        t = threading.Thread(target=start_tracker, daemon=True)
        t.start()
        start_dashboard()
