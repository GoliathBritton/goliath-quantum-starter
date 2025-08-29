"""
Audit log for all pricing changes. Call this from CI or sync script.
Appends timestamped JSON to docs/pricing_history.jsonl
"""
import json
from pathlib import Path
from datetime import datetime

PRICING_JSON = Path(__file__).parent.parent / "docs" / "pricing.json"
PRICING_HISTORY = Path(__file__).parent.parent / "docs" / "pricing_history.jsonl"

def log_pricing_change():
    with open(PRICING_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    entry = {"timestamp": datetime.utcnow().isoformat() + "Z", "pricing": data}
    with open(PRICING_HISTORY, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"Logged pricing change at {entry['timestamp']}")

if __name__ == "__main__":
    log_pricing_change()
