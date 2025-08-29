"""
Streamlit dashboard for Goliath of All Trade: Quantum+AI Automations
- Division selector, demo workflows, and automation runner for each business unit
"""

import streamlit as st
from nqba import AUTOMATIONS, DIVISIONS

st.set_page_config(page_title="NQBA Quantum+AI Automation Demo", layout="wide")
st.title("Goliath of All Trade: Quantum+AI Automation Platform")

# Division selector
st.sidebar.header("Business Divisions")
div_keys = list(DIVISIONS.keys())
div_labels = [DIVISIONS[k]["label"] for k in div_keys]
div_idx = st.sidebar.selectbox(
    "Select Division", range(len(div_keys)), format_func=lambda i: div_labels[i]
)
div_key = div_keys[div_idx]
division = DIVISIONS[div_key]

st.header(division["label"])

# Demo workflows for this division
st.subheader("Demo Workflows")
for wf in division["demo_workflows"]:
    with st.expander(wf["name"] + ": " + wf["description"]):
        if st.button(f"Run Demo: {wf['name']}"):
            result = wf["run"]()
            st.json(result)

st.sidebar.header("Available Automations")
auto_names = division["automations"]
selected = st.sidebar.selectbox("Choose an automation", auto_names)

st.subheader(f"Automation: {selected}")

# Dynamic input form based on automation type (scoped to division automations)
if selected == "lead_scoring":
    lead_score = st.number_input("Lead Score", 0.0, 1.0, 0.8)
    risk = st.number_input("Risk", 0.0, 1.0, 0.1)
    if st.button("Run Lead Scoring"):
        result = AUTOMATIONS[selected]({"lead_score": lead_score, "risk": risk})
        st.json(result)
elif selected == "quantum_optimize":
    st.write("QUBO: x0^2 + x1^2 + 0.5*x0*x1")
    Q = [(0, 0, 1.0), (1, 1, -1.0), (0, 1, 0.5)]
    if st.button("Run Quantum Optimization"):
        result = AUTOMATIONS[selected](2, Q)
        st.json(result)
elif selected == "sales_script":
    name = st.text_input("Customer Name", "Alice")
    if st.button("Generate Script"):
        result = AUTOMATIONS[selected]({"name": name})
        st.json(result)
elif selected == "openai_chat":
    prompt = st.text_area("Prompt", "What is quantum AI?")
    if st.button("Run OpenAI Chat"):
        result = AUTOMATIONS[selected](prompt)
        st.json(result)
else:
    st.info("Demo input form not yet implemented for this automation.")
    if st.button("Run Automation (no input)"):
        try:
            result = AUTOMATIONS[selected]()
            st.json(result)
        except Exception as e:
            st.error(str(e))
