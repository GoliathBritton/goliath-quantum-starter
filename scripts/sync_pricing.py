"""
Syncs pricing.md and pricing.json for developer/design parity.
- Converts pricing.json to Markdown/HTML for docs/pricing.md
- Converts pricing.md to JSON for design/Framer export (if needed)
"""
import json
from pathlib import Path

PRICING_JSON = Path(__file__).parent.parent / "docs" / "pricing.json"
PRICING_MD = Path(__file__).parent.parent / "docs" / "pricing.md"


def json_to_md(data):
    md = [f"# 🪙 {data['hero']['title']}\n"]
    md.append(f"> {data['hero']['subtitle']}\n")
    md.append("\n**[🚀 See Live Demos]({}) | [📞 Book a Discovery Call]({})**\n".format(
        data['hero']['cta'][0]['href'], data['hero']['cta'][1]['href']))
    md.append(f"\n## {data['onramp']['title']}\n")
    for feat in data['onramp']['features']:
        md.append(f"- {feat}")
    md.append(f"\n[**{data['onramp']['cta']['label']}**]({data['onramp']['cta']['href']}})\n")
    md.append(f"\n## 💎 Quantum Luxury Tiers\n")
    for tier in data['tiers']:
        md.append(f"### {tier['name']} — {tier['price']}")
        md.append(f"_{tier['desc']}_\n")
        for feat in tier['features']:
            md.append(f"- {feat}")
        md.append(f"\n[**{tier['cta']['label']}**]({tier['cta']['href']})\n")
    md.append(f"\n## {data['upsells']['title']}\n")
    for item in data['upsells']['items']:
        md.append(f"- {item}")
    md.append(f"\n## {data['successFees']['title']}\n")
    for item in data['successFees']['items']:
        md.append(f"- {item}")
    md.append(f"\n## {data['investors']['title']}\n")
    md.append(f"> {data['investors']['desc']}\n")
    md.append(f"\n[**{data['investors']['cta']['label']}**]({data['investors']['cta']['href']})\n")
    return "\n".join(md)


def main():
    with open(PRICING_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    md = json_to_md(data)
    with open(PRICING_MD, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Synced {PRICING_JSON} -> {PRICING_MD}")

if __name__ == "__main__":
    main()
