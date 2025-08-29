"""
Slack bot for querying live pricing via /pricing command.
Requires: pip install slack_bolt
Set SLACK_BOT_TOKEN and SLACK_APP_TOKEN env vars.
"""

import os
import json
from slack_bolt import App
from pathlib import Path
import requests

PRICING_API = os.environ.get("PRICING_API", "http://localhost:8000/pricing")

app = App(token=os.environ["SLACK_BOT_TOKEN"], app_token=os.environ["SLACK_APP_TOKEN"])


@app.command("/pricing")
def handle_pricing(ack, respond, command):
    ack()
    try:
        r = requests.get(PRICING_API)
        data = r.json()
        tiers = data.get("tiers", [])
        msg = "*Current Pricing Tiers:*\n"
        for t in tiers:
            msg += f"• *{t['name']}* — {t['price']} ({t['desc']})\n"
        respond(msg)
    except Exception as e:
        respond(f"Error fetching pricing: {e}")


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
