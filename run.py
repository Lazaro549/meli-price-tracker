"""
Entry point for GitHub Actions.
Runs a single price-check pass (no loop) and exits.
"""
from tracker.db import init_db
from tracker.scheduler import run_once

if __name__ == "__main__":
    init_db()
    print("🔄 Running price check...")
    run_once()
    print("✅ Done.")
