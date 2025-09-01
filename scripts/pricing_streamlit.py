from src.branding import BRANDING
import streamlit as st


def show_branding():
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.image(BRANDING["goliath"]["logo"], width=180)
        st.caption(BRANDING["goliath"]["tagline"])
    with col2:
        st.image(BRANDING["flyfox"]["logo"], width=120)
        st.caption(BRANDING["flyfox"]["tagline"])
    with col3:
        st.image(BRANDING["sigma_select"]["logo"], width=120)
        st.caption(BRANDING["sigma_select"]["tagline"])
    st.markdown(
        f"<div style='text-align:center; color:#888; font-size:0.9em;'>"
        f"<b>{BRANDING['goliath']['name']} | {BRANDING['flyfox']['name']} | {BRANDING['sigma_select']['name']}</b><br>"
        f"{BRANDING['goliath']['tagline']} | {BRANDING['flyfox']['tagline']} | {BRANDING['sigma_select']['tagline']}"
        f"</div>",
        unsafe_allow_html=True,
    )


"""
Streamlit app to display synchronized pricing from docs/pricing.json
Run with: streamlit run scripts/pricing_streamlit.py
"""
import json
from pathlib import Path
import streamlit as st

PRICING_JSON = Path(__file__).parent.parent / "docs" / "pricing.json"


def load_pricing():
    with open(PRICING_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    show_branding()
    data = load_pricing()
    st.title(data["hero"]["title"])
    st.markdown(f"> {data['hero']['subtitle']}\n")
    st.markdown(
        " ".join([f"[{cta['label']}]({cta['href']})" for cta in data["hero"]["cta"]])
    )

    st.header(data["onramp"]["title"])
    st.markdown("\n".join([f"- {f}" for f in data["onramp"]["features"]]))
    st.markdown(f"[{data['onramp']['cta']['label']}]({data['onramp']['cta']['href']})")

    st.header("💎 Quantum Luxury Tiers")
    for tier in data["tiers"]:
        st.subheader(f"{tier['name']} — {tier['price']}")
        st.caption(tier["desc"])
        st.markdown("\n".join([f"- {f}" for f in tier["features"]]))
        st.markdown(f"[{tier['cta']['label']}]({tier['cta']['href']})")

    st.header(data["upsells"]["title"])
    st.markdown("\n".join([f"- {i}" for i in data["upsells"]["items"]]))

    st.header(data["successFees"]["title"])
    st.markdown("\n".join([f"- {i}" for i in data["successFees"]["items"]]))

    st.header(data["investors"]["title"])
    st.markdown(f"> {data['investors']['desc']}")
    st.markdown(
        f"[{data['investors']['cta']['label']}]({data['investors']['cta']['href']})"
    )


if __name__ == "__main__":
    main()
