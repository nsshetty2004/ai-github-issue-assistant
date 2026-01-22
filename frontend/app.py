import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# -------------------------------------------------
# Environment
# -------------------------------------------------
load_dotenv()
BACKEND_API_KEY = os.getenv("BACKEND_API_KEY")
BACKEND_URL = "http://127.0.0.1:8000/analyze"

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="AI GitHub Issue Assistant",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------------------------
# Global Background
# -------------------------------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #f8fafc, #eef2ff);
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Custom CSS (Futuristic + Professional)
# -------------------------------------------------
st.markdown("""
<style>

/* -------- Animated Gradient Title -------- */
@keyframes gradientMove {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.main-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(90deg, #4F46E5, #22C55E, #6366F1);
    background-size: 300% 300%;
    animation: gradientMove 6s ease infinite;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    color: #6b7280;
    font-size: 1.05rem;
}

/* -------- Glassmorphism Cards -------- */
.card {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    padding: 1.6rem;
    border-radius: 14px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.08);
    margin-bottom: 1.5rem;
}

/* -------- Labels -------- */
.label-chip {
    display: inline-block;
    padding: 6px 12px;
    margin: 4px 6px 4px 0;
    background-color: #eef2ff;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 600;
}

/* -------- Priority Badges -------- */
.badge {
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 700;
}

.badge-critical { background:#fee2e2; color:#991b1b; }
.badge-high { background:#ffedd5; color:#9a3412; }
.badge-medium { background:#fef3c7; color:#92400e; }
.badge-low { background:#dcfce7; color:#166534; }

/* -------- Agent Pulse -------- */
@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(34,197,94,0.6); }
  70% { box-shadow: 0 0 0 10px rgba(34,197,94,0); }
  100% { box-shadow: 0 0 0 0 rgba(34,197,94,0); }
}

.agent-badge {
    background-color:#dcfce7;
    color:#166534;
    padding:6px 14px;
    border-radius:999px;
    font-size:0.8rem;
    font-weight:700;
    animation: pulse 2.5s infinite;
}

.signal {
    font-size: 0.9rem;
    color:#374151;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown('<div class="main-title">🤖 AI-Powered GitHub Issue Assistant</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Reliability-first agent for triaging GitHub issues</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div style="margin-top:10px;">
<span class="agent-badge">🟢 Agent Online · Deterministic Mode Enabled</span>
</div>
""", unsafe_allow_html=True)

st.write("")

# -------------------------------------------------
# Layout
# -------------------------------------------------
left_col, right_col = st.columns([1, 2])

# -------------------------------------------------
# LEFT: Input + AI Explanation
# -------------------------------------------------
with left_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔍 Issue Input")

    repo_url = st.text_input(
        "GitHub Repository URL",
        placeholder="https://github.com/facebook/react"
    )

    issue_number = st.number_input(
        "Issue Number",
        min_value=1,
        step=1
    )

    show_reasoning = st.checkbox("🧠 Show agent signals", value=True)
    analyze_btn = st.button("🚀 Run AI Analysis", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ---- How AI Works Box ----
    st.markdown("""
    <div class="card">
    <b>🧠 How This AI Analysis Works</b>
    <ol style="margin-top:8px; color:#4b5563; font-size:0.9rem;">
        <li>📥 Fetches issue title, body, and comments</li>
        <li>🔍 Detects bug or feature signals</li>
        <li>📊 Assigns a priority score (1–5)</li>
        <li>🧾 Ensures schema-safe JSON output</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# RIGHT: Results
# -------------------------------------------------
with right_col:
    if analyze_btn:
        if not repo_url:
            st.warning("Please enter a valid GitHub repository URL.")
        else:
            with st.spinner("🔄 Fetching → Analyzing → Validating"):
                try:
                    response = requests.get(
                        BACKEND_URL,
                        params={"repo_url": repo_url, "issue_number": issue_number},
                        headers={"x-api-key": BACKEND_API_KEY},
                        timeout=120
                    )

                    if response.status_code == 200:
                        data = response.json()
                        priority = data["priority_score"]

                        if priority >= 4:
                            severity = ("Critical", "badge-critical")
                        elif priority == 3:
                            severity = ("High", "badge-high")
                        elif priority == 2:
                            severity = ("Medium", "badge-medium")
                        else:
                            severity = ("Low", "badge-low")

                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.subheader("🧠 AI Analysis")

                        st.markdown("**📌 Summary**")
                        st.write(data["summary"])

                        st.markdown("**🏷️ Issue Type**")
                        st.write(data["type"].replace("_", " ").title())

                        st.markdown("**🚦 Priority Score**")
                        st.markdown(
                            f'<span class="badge {severity[1]}">{severity[0]} (Score: {priority}/5)</span>',
                            unsafe_allow_html=True
                        )

                        st.markdown("**⚠️ Potential Impact**")
                        st.write(data["potential_impact"])

                        st.markdown("**🔖 Suggested Labels**")
                        for label in data["suggested_labels"]:
                            st.markdown(f'<span class="label-chip">{label}</span>', unsafe_allow_html=True)

                        if show_reasoning:
                            st.markdown("**🧩 Signals Detected**")
                            signals = []
                            title = data["summary"].lower()

                            if any(k in title for k in ["error", "fail", "crash", "exception"]):
                                signals.append("Error / failure language detected")
                            if priority >= 4:
                                signals.append("Runtime-blocking behavior inferred")
                            if not signals:
                                signals.append("Feature or improvement request detected")

                            for s in signals:
                                st.markdown(f"• {s}")

                        st.markdown('</div>', unsafe_allow_html=True)

                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.subheader("📦 Raw JSON Output")

                        formatted_json = json.dumps(data, indent=2)
                        st.code(formatted_json, language="json")

                        st.download_button(
                            "📋 Copy JSON",
                            formatted_json,
                            "issue_analysis.json",
                            "application/json"
                        )

                        st.markdown('</div>', unsafe_allow_html=True)

                    else:
                        st.error(response.text)

                except Exception as e:
                    st.error(f"Backend error: {e}")

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown("""
<hr style="margin-top:40px;">
<div style="text-align:center; color:#6b7280; font-size:0.8rem;">
AI-Powered GitHub Issue Assistant · Built with FastAPI & Streamlit · Reliability-First AI Design
</div>
""", unsafe_allow_html=True)
