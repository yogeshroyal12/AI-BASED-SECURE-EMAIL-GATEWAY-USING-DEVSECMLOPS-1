from __future__ import annotations

import json
import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[2]
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
API_KEY = os.getenv("API_KEY", "change-me")
MODEL_META = ROOT / "02_DEVELOP_BUILD" / "model" / "model_metadata.json"
DRIFT_REPORT = ROOT / "04_DEPLOY_MONITOR" / "monitoring" / "drift_report.json"


st.set_page_config(
    page_title="Secure Email Gateway",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container { padding-top: 1.2rem; padding-bottom: 2rem; }
    .hero {
        padding: 1.5rem 1.7rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #111827 0%, #1f3b70 55%, #2563eb 100%);
        color: white;
        box-shadow: 0 10px 30px rgba(15,23,42,.22);
        margin-bottom: 1rem;
    }
    .hero h1 { margin: 0; font-size: 2.2rem; }
    .hero p { margin: .45rem 0 0; color: #dbeafe; }
    .metric-card {
        padding: 1rem;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        background: #ffffff;
        box-shadow: 0 4px 15px rgba(15,23,42,.06);
        min-height: 110px;
    }
    .metric-title { font-size: .83rem; color: #64748b; }
    .metric-value { font-size: 1.8rem; font-weight: 700; margin-top: .2rem; }
    .decision {
        border-radius: 18px;
        padding: 1.25rem;
        border: 1px solid #e2e8f0;
        background: #f8fafc;
    }
    .small-note { color: #64748b; font-size: .82rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h1>🛡️ AI-Based Secure Email Gateway</h1>
      <p>ML classification + runtime protection + DevSecMLOps monitoring</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("⚙️ Connection")
    api_url = st.text_input("FastAPI URL", API_BASE_URL)
    api_key = st.text_input("API Key", API_KEY, type="password")
    st.caption("Production should use a strong secret, not the demo key.")
    st.divider()
    st.markdown("### Exam coverage")
    st.write("✅ Plan & Design")
    st.write("✅ Develop & Build")
    st.write("✅ Test & Verify")
    st.write("✅ Deploy & Monitor")


def headers():
    return {"X-API-Key": api_key}


def api_get(path: str, **kwargs):
    return requests.get(f"{api_url}{path}", headers=headers(), timeout=8, **kwargs)


def api_post(path: str, payload: dict):
    return requests.post(f"{api_url}{path}", json=payload, headers=headers(), timeout=12)


tab1, tab2, tab3, tab4 = st.tabs(
    ["✉️ Live Email Analysis", "📊 Security Dashboard", "🚨 Audit & Incidents", "🧠 Model & Drift"]
)

with tab1:
    st.subheader("Analyze an email")
    col1, col2 = st.columns([1, 1])
    with col1:
        sample = st.selectbox(
            "Load a demo example",
            ["Custom", "SAFE", "SPAM", "PHISHING"],
        )
        samples = {
            "SAFE": (
                "Project meeting reminder",
                "Hi team, our engineering meeting is scheduled for tomorrow at 10 AM. Please bring the project status update.",
            ),
            "SPAM": (
                "Congratulations! You won",
                "You have been selected for a special reward. Claim the limited-time promotional offer today.",
            ),
            "PHISHING": (
                "Urgent account verification",
                "Your account has been suspended. Click here immediately to verify your password and restore access.",
            ),
        }
        default_subject = samples.get(sample, ("", ""))[0]
        default_body = samples.get(sample, ("", ""))[1]
        subject = st.text_input("Subject", value=default_subject, max_chars=200)
        body = st.text_area(
            "Email body",
            value=default_body,
            height=220,
            max_chars=10000,
            placeholder="Paste the email body here...",
        )
    with col2:
        st.markdown("#### What the system demonstrates")
        st.info(
            "The request passes authentication, validation and rate limiting before the ML model is called."
        )
        st.markdown(
            """
            **Decision logic**
            - SAFE → ALLOW
            - SPAM → QUARANTINE
            - PHISHING → BLOCK
            """
        )
        st.caption("Full email bodies are not stored in the audit log; only a SHA-256 fingerprint is recorded.")

    if st.button("🔍 Analyze Email", type="primary", use_container_width=True):
        if not subject.strip() or not body.strip():
            st.error("Subject and body are required.")
        else:
            try:
                with st.spinner("Running secure analysis..."):
                    response = api_post("/analyze-email", {"subject": subject, "body": body})

                if response.status_code == 200:
                    result = response.json()
                    st.success("Analysis completed.")
                    cards = st.columns(4)
                    cards[0].metric("Prediction", result["prediction"])
                    cards[1].metric("Probability", f"{result['probability']*100:.1f}%")
                    cards[2].metric("Risk", result["risk"])
                    cards[3].metric("Action", result["action"])

                    st.markdown("### Security explanation")
                    st.markdown('<div class="decision">', unsafe_allow_html=True)
                    if result["reasons"]:
                        for reason in result["reasons"]:
                            st.write(f"• {reason}")
                    else:
                        st.write("• No configured risk indicators were detected.")
                    st.write(f"Request ID: `{result['request_id']}`")
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error(f"API error {response.status_code}: {response.text}")
            except requests.RequestException as exc:
                st.error(f"Could not connect to FastAPI: {exc}")

with tab2:
    st.subheader("Live operational metrics")
    refresh = st.button("↻ Refresh metrics")
    try:
        stats_response = api_get("/admin/stats")
        if stats_response.status_code == 200:
            stats = stats_response.json()
            cards = st.columns(7)
            metrics = [
                ("Total", stats["total_events"]),
                ("Safe", stats["safe"]),
                ("Spam", stats["spam"]),
                ("Phishing", stats["phishing"]),
                ("Allowed", stats["allowed"]),
                ("Quarantine", stats["quarantined"]),
                ("Blocked", stats["blocked"]),
            ]
            for card, (title, value) in zip(cards, metrics):
                card.markdown(
                    f'<div class="metric-card"><div class="metric-title">{title}</div>'
                    f'<div class="metric-value">{value}</div></div>',
                    unsafe_allow_html=True,
                )

            chart_left, chart_right = st.columns(2)
            with chart_left:
                distribution = pd.DataFrame(
                    {
                        "Prediction": ["SAFE", "SPAM", "PHISHING"],
                        "Count": [stats["safe"], stats["spam"], stats["phishing"]],
                    }
                )
                fig = px.bar(distribution, x="Prediction", y="Count", title="Prediction distribution")
                st.plotly_chart(fig, use_container_width=True)
            with chart_right:
                actions = pd.DataFrame(
                    {
                        "Action": ["ALLOW", "QUARANTINE", "BLOCK"],
                        "Count": [stats["allowed"], stats["quarantined"], stats["blocked"]],
                    }
                )
                fig = px.pie(actions, names="Action", values="Count", title="Security actions")
                st.plotly_chart(fig, use_container_width=True)

            st.caption(f"Security events recorded: {stats['security_events']}")
        else:
            st.warning(f"Stats endpoint returned {stats_response.status_code}.")
    except requests.RequestException as exc:
        st.error(f"Could not connect to FastAPI: {exc}")

with tab3:
    st.subheader("Audit & incident evidence")
    try:
        audit_response = api_get("/admin/audit?limit=30")
        sec_response = api_get("/admin/security-events?limit=30")
        if audit_response.status_code == 200:
            audit = audit_response.json()
            st.markdown("#### Recent email decisions")
            st.dataframe(pd.DataFrame(audit), use_container_width=True, hide_index=True)
        if sec_response.status_code == 200:
            incidents = sec_response.json()
            st.markdown("#### Recent security events")
            if incidents:
                st.dataframe(pd.DataFrame(incidents), use_container_width=True, hide_index=True)
            else:
                st.info("No security events recorded yet.")
    except requests.RequestException as exc:
        st.error(f"Could not load audit data: {exc}")

with tab4:
    st.subheader("Model governance")
    try:
        model_response = api_get("/admin/model-info")
        if model_response.status_code == 200:
            info = model_response.json()
            cols = st.columns(4)
            cols[0].metric("Version", info["version"])
            cols[1].metric("Algorithm", "TF-IDF + Logistic Reg.")
            cols[2].metric("Accuracy", f"{info['metrics']['accuracy']*100:.1f}%")
            cols[3].metric("Weighted F1", f"{info['metrics']['weighted_f1']*100:.1f}%")
            st.code(json.dumps(info, indent=2), language="json")
        else:
            st.warning("Model information could not be loaded.")

        st.markdown("#### Basic drift monitoring")
        if DRIFT_REPORT.exists():
            drift = json.loads(DRIFT_REPORT.read_text(encoding="utf-8"))
            if drift.get("status") == "DRIFT_DETECTED":
                st.warning("Potential feature drift detected in the sample batch.")
            else:
                st.success("No drift detected in the included sample batch.")
            st.json(drift)
        else:
            st.info("Run the drift check script to generate the report.")
    except requests.RequestException as exc:
        st.error(f"Could not load model information: {exc}")

st.divider()
st.caption("DevSecMLOps practical demo • Secure by design • Built for VS Code")
