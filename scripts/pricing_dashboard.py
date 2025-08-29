import streamlit_chat
import streamlit_feedback
import openai
## Onboarding, PDF, Excel export: custom/native fallback, package not found
import streamlit_authenticator as stauth
import pytz
import babel
import pdfkit
import xlsxwriter
import websockets
import requests
import random
def ai_solutions_builder(lang):
    st.header("🤖 Build AI Solutions" if lang == "en" else "🤖 Crear Soluciones de IA")
    st.markdown("""Design, test, and deploy custom AI-powered pricing or business solutions.\n
    - Use OpenAI or custom models\n    - Integrate with your data\n    - Deploy as API or dashboard widget\n    """ if lang == "en" else """Diseña, prueba y lanza soluciones de IA personalizadas para precios o negocio.\n- Usa OpenAI o modelos propios\n- Integra tus datos\n- Despliega como API o widget\n""")
    prompt = st.text_area("Describe your AI solution (e.g., 'Suggest optimal plan for user X')", key="ai_prompt")
    if st.button("Generate Solution" if lang == "en" else "Generar Solución"):
        st.info("[Stub] AI solution generated! (Connect OpenAI API for real output)")
"""
Advanced Streamlit dashboard for pricing, with filtering, search, and tier highlighting.
Run with: streamlit run scripts/pricing_dashboard.py
from src.branding import BRANDING
"""

import json
from pathlib import Path
import streamlit as st

import plotly.graph_objs as go
import pandas as pd
import getpass
import smtplib
from email.message import EmailMessage
import streamlit.components.v1 as components
from src.branding import BRANDING
def contact_sales_form(lang):
    st.header("📞 Contact Sales" if lang == "en" else "📞 Contactar Ventas")
    with st.form("contact_sales_form"):
        name = st.text_input("Your Name" if lang == "en" else "Tu Nombre", key="name")
        email = st.text_input("Your Email" if lang == "en" else "Tu Correo", key="email")
        message = st.text_area("Message" if lang == "en" else "Mensaje", key="msg")
        submitted = st.form_submit_button("Send" if lang == "en" else "Enviar")
        if submitted:
            try:
                msg = EmailMessage()
                msg["Subject"] = f"[{BRANDING['goliath']['name']} | {BRANDING['flyfox']['name']} | {BRANDING['sigma_select']['name']}] Sales Inquiry from {name}"
                msg["From"] = email
                msg["To"] = "sales@example.com"
                msg.set_content(f"{message}\n\n--\n{BRANDING['goliath']['name']} | {BRANDING['flyfox']['name']} | {BRANDING['sigma_select']['name']}\n{BRANDING['goliath']['tagline']} | {BRANDING['flyfox']['tagline']} | {BRANDING['sigma_select']['tagline']}")
                # Uncomment and configure SMTP for real use
                # with smtplib.SMTP('localhost') as s:
                #     s.send_message(msg)
                st.success("Thank you! Our team will contact you soon." if lang == "en" else "¡Gracias! Nuestro equipo te contactará pronto.")
            except Exception:
                st.warning("Message not sent (demo mode)" if lang == "en" else "Mensaje no enviado (modo demo)")
def show_testimonials(data, lang):
    st.header("💬 What Our Clients Say" if lang == "en" else "💬 Opiniones de Clientes")
    testimonials = data.get("testimonials", [])
    if testimonials:
        idx = st.session_state.get("testimonial_idx", 0)
        t = testimonials[idx % len(testimonials)]
        st.markdown(f'> "{t["quote"]}" — **{t["name"]}**')
        if t.get("logo"):
            st.image(f'./docs/{t["logo"]}', width=80)
        col1, col2 = st.columns([1,1])
        with col1:
            if st.button("⬅️" if lang == "en" else "Anterior", key="prev_testimonial"):
                st.session_state["testimonial_idx"] = (idx - 1) % len(testimonials)
                st.experimental_rerun()
        with col2:
            if st.button("➡️" if lang == "en" else "Siguiente", key="next_testimonial"):
                st.session_state["testimonial_idx"] = (idx + 1) % len(testimonials)
                st.experimental_rerun()

def show_case_studies(data, lang):
    st.header("📚 Case Studies" if lang == "en" else "📚 Casos de Éxito")
    cases = data.get("caseStudies", [])
    if cases:
        idx = st.session_state.get("case_idx", 0)
        c = cases[idx % len(cases)]
        st.markdown(f'**{c["title"]}**: {c["summary"]}')
        col1, col2 = st.columns([1,1])
        with col1:
            if st.button("⬅️" if lang == "en" else "Anterior", key="prev_case"):
                st.session_state["case_idx"] = (idx - 1) % len(cases)
                st.experimental_rerun()
        with col2:
            if st.button("➡️" if lang == "en" else "Siguiente", key="next_case"):
                st.session_state["case_idx"] = (idx + 1) % len(cases)
                st.experimental_rerun()

def show_customer_logos(data, lang):
    st.header("🏢 Trusted By" if lang == "en" else "🏢 Clientes")
    logos = data.get("customerLogos", [])
    cols = st.columns(min(4, len(logos))) if logos else []
    for i, logo in enumerate(logos):
        with cols[i % len(cols)]:
            st.image(f'./docs/{logo}', width=80)

PRICING_JSON = Path(__file__).parent.parent / "docs" / "pricing.json"
PRICING_HISTORY = Path(__file__).parent.parent / "docs" / "pricing_history.jsonl"

def load_pricing():
    with open(PRICING_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

def load_history():
    if not PRICING_HISTORY.exists():
        return []
    with open(PRICING_HISTORY, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def admin_login():
    st.sidebar.header("Admin Login")
    user = st.sidebar.text_input("Username")
    pw = st.sidebar.text_input("Password", type="password")
    if user == "admin" and pw == "adminpass":
        st.session_state["admin"] = True
        st.sidebar.success("Admin logged in!")
    elif user or pw:
        st.sidebar.error("Invalid credentials")

def main():
    # Theme toggle
    theme = st.sidebar.radio("Theme", ["Light", "Dark"], index=0)
    if theme == "Dark":
        st.markdown("""
            <style>
            body, .stApp { background: #181818 !important; color: #f0f0f0 !important; }
            .stButton>button { background: #222; color: #fff; }
            </style>
        """, unsafe_allow_html=True)

    # Branding: Goliath, Fly Fox, Sigma Select
    st.sidebar.image(BRANDING["goliath"]["logo"], width=120)
    st.sidebar.markdown(f"**{BRANDING['goliath']['name']}**")
    st.sidebar.caption(BRANDING['goliath']['tagline'])
    st.sidebar.image(BRANDING["flyfox"]["logo"], width=100)
    st.sidebar.caption(BRANDING['flyfox']['tagline'])
    st.sidebar.image(BRANDING["sigma_select"]["logo"], width=100)
    st.sidebar.caption(BRANDING['sigma_select']['tagline'])

    # SSO/Authentication (stub)
    st.session_state["role"] = st.sidebar.selectbox("Role", ["client", "admin", "sales", "investor"], index=0)
    st.sidebar.info("[Stub] SSO/Authenticator integration here.")

    # Onboarding
    if st.sidebar.button("Show Onboarding" if lang == "en" else "Mostrar Guía"):
        st.info("Welcome to the dashboard! [Onboarding steps would appear here.]")

    # Live Chat
    if st.sidebar.button("Live Chat" if lang == "en" else "Chat en Vivo"):
        streamlit_chat.chat("How can we help you?" if lang == "en" else "¿En qué podemos ayudarte?")

    # Feedback
    if st.sidebar.button("Feedback" if lang == "en" else "Sugerencias"):
        streamlit_feedback.feedback()

    # PWA install prompt (stub)
    st.sidebar.info("[Stub] Install as PWA for offline access!")
    # Accessibility: ARIA roles, color contrast, keyboard nav
    st.markdown('<div role="main" aria-label="Pricing Dashboard">', unsafe_allow_html=True)
    st.info("Tip: Use Tab/Shift+Tab to navigate. All controls are keyboard accessible.")
    # Localization/i18n (English/Spanish, can extend)
    lang = st.sidebar.selectbox("Language", ["en", "es"], index=0, help="Select language / Selecciona idioma")
    st.set_page_config(page_title="Quantum Pricing Dashboard", layout="wide")
    if "admin" not in st.session_state:
        st.session_state["admin"] = False
    admin_login()
    data = load_pricing()
    st.title(data['hero']['title'])
    st.markdown(f"> {data['hero']['subtitle']}\n")
    st.markdown(" ".join([f"[{cta['label']}]({cta['href']})" for cta in data['hero']['cta']]))


    st.header(data['onramp']['title'] if lang == "en" else "✨ Acceso Gratuito")
    st.markdown("\n".join([f"- {f}" for f in data['onramp']['features']]))
    st.markdown(f"[{data['onramp']['cta']['label']}]({data['onramp']['cta']['href']})")

    st.header("💎 Quantum Luxury Tiers" if lang == "en" else "💎 Niveles de Lujo Cuántico")
    tiers = data['tiers']
    tier_names = [t['name'] for t in tiers]
    selected = st.multiselect("Show Tiers", tier_names, default=tier_names)
    search = st.text_input("Search features or price", "")
    for tier in tiers:
        if tier['name'] not in selected:
            continue
        if search and not (search.lower() in tier['name'].lower() or search.lower() in tier['desc'].lower() or any(search.lower() in f.lower() for f in tier['features'])):
            continue
        st.subheader(f"{tier['name']} — {tier['price']}")
        st.caption(tier['desc'])
        st.markdown("\n".join([f"- {f}" for f in tier['features']]))
        st.markdown(f"[{tier['cta']['label']}]({tier['cta']['href']})")
        if tier.get('highlight'):
            st.markdown(":star: **Recommended**")
        if tier.get('premium'):
            st.markdown(":crown: **Premium**")
        if tier.get('ultra'):
            st.markdown(":rocket: **Ultra**")

    # --- Plotly chart for pricing trends ---
    st.header("📈 Pricing Trends")
    history = load_history()
    if history:
        df = pd.DataFrame([
            {"timestamp": h["timestamp"], **{t["name"]: t["price"] for t in h["pricing"].get("tiers", [])}}
            for h in history
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")
        for tier in tier_names:
            if tier in df:
                st.plotly_chart(go.Figure([go.Scatter(x=df["timestamp"], y=df[tier], mode="lines+markers", name=tier)]), use_container_width=True)

    # --- Export to CSV/PDF ---
    st.header("Export Pricing Data" if lang == "en" else "Exportar Datos de Precios")
    if st.button("Export CSV"):
        st.download_button("Download CSV", df.to_csv(index=False), file_name="pricing_history.csv")
    # PDF export would require more setup (e.g., pdfkit)

    # --- What's New / Changelog widget ---
    st.header("🆕 What's New (Changelog)" if lang == "en" else "🆕 Novedades")
    if history:
        for h in reversed(history[-5:]):
            st.markdown(f"- {h['timestamp']}: Pricing updated")

    st.header(data['upsells']['title'] if lang == "en" else "🏛 Servicios Adicionales")
    st.markdown("\n".join([f"- {i}" for i in data['upsells']['items']]))

    st.header(data['successFees']['title'] if lang == "en" else "📈 Tarifas de Éxito")
    st.markdown("\n".join([f"- {i}" for i in data['successFees']['items']]))

    st.header(data['investors']['title'] if lang == "en" else "👑 Acceso para Inversores")

    st.markdown(f"> {data['investors']['desc']}")
    st.markdown(f"[{data['investors']['cta']['label']}]({data['investors']['cta']['href']})")


    # Real-time pricing updates (stub)
    st.info("[Stub] Real-time pricing updates enabled.")

    # Role-based dashboard views
    role = st.session_state["role"]
    if role == "admin":
        st.success("Admin analytics and controls visible.")
    elif role == "sales":
        st.info("Sales dashboard view.")
    elif role == "investor":
        st.info("Investor dashboard view.")

    # Multi-currency support (stub)
    currency = st.sidebar.selectbox("Currency", ["USD", "EUR", "GBP", "JPY"], index=0)
    st.info(f"[Stub] Showing prices in {currency}.")

    # Accessibility audit (stub)
    if st.sidebar.button("Accessibility Audit"):
        st.info("[Stub] Accessibility audit report downloaded.")

    # Export to PDF/Excel
    if st.sidebar.button("Export PDF"):
        st.info("[TODO] PDF export coming soon. Use browser print to PDF as a workaround.")
    if st.sidebar.button("Export Excel"):
        st.info("[TODO] Excel export coming soon. Use CSV export for now.")

    # API usage analytics (stub)
    if role == "admin":
        st.info("[Stub] API usage analytics chart here.")

    # Automated changelog digest (stub)
    if st.sidebar.button("Send Changelog Digest"):
        st.info("[Stub] Changelog digest sent to subscribers.")

    # AI-powered pricing recommendations (stub)
    if st.sidebar.button("AI Pricing Recommendation"):
        st.info("[Stub] AI recommends optimal plan: Quantum Pro.")

    show_testimonials(data, lang)
    show_case_studies(data, lang)
    show_customer_logos(data, lang)
    contact_sales_form(lang)
    ai_solutions_builder(lang)

    # Footer: compliance, contact, copyright
    st.markdown("""
    <footer style='margin-top:2em; text-align:center; color:gray;'>
    <small>
    &copy; 2025 Goliath Quantum. <a href='mailto:compliance@goliathquantum.com'>compliance@goliathquantum.com</a> | <a href='/privacy'>Privacy</a> | <a href='/accessibility'>Accessibility</a>
    </small>
    </footer>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state["admin"]:
        st.success("Admin features enabled.")
        # Add more admin features here

if __name__ == "__main__":
    main()
