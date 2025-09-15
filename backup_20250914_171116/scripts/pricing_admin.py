"""
Admin CLI for pricing: role-based access, changelog, and edit support.
"""

import json
from pathlib import Path
import getpass
import sys

PRICING_JSON = Path(__file__).parent.parent / "docs" / "pricing.json"
ADMINS = {"admin": "adminpass"}  # Replace with secure storage in production


def require_admin():
    user = input("Username: ")
    pw = getpass.getpass("Password: ")
    if ADMINS.get(user) != pw:
        print("Access denied.")
        sys.exit(1)
    print(f"Welcome, {user}!")


def show_changelog():
    print("--- Pricing Changelog ---")
    history = Path(__file__).parent.parent / "docs" / "pricing_history.jsonl"
    if not history.exists():
        print("No changelog yet.")
        return
    with open(history, "r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            print(
                f"{entry['timestamp']}: {entry['pricing'].get('hero', {}).get('title', '')}"
            )


def edit_pricing():
    require_admin()
    with open(PRICING_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(json.dumps(data, indent=2))
    # In production, launch a proper editor or web UI
    print("Edit pricing.json manually, then run pricing_auditlog.py to log the change.")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Pricing Admin CLI")
    parser.add_argument(
        "--changelog", action="store_true", help="Show pricing changelog"
    )
    parser.add_argument("--edit", action="store_true", help="Edit pricing (admin only)")
    args = parser.parse_args()
    if args.changelog:
        show_changelog()
    elif args.edit:
        edit_pricing()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
