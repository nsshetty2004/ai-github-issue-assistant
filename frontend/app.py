import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="AI GitHub Issue Assistant",
    page_icon="🤖",
    layout="centered"
)

# -------------------------------------------------
# Custom CSS
# -------------------------------------------------
st.markdown("""
<style>
.main-title {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(90deg, #4F46E5, #22C55E);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    color: #6b7280;
    font-size: 1.05rem;
}

.card {
    background-color: #ffffff;
    padding: 1.5rem;
    border-radius: 14px;
    box-shadow: 0px 8px 24px rgba(0,0,0,0.05);
    margin-bottom: 1.5rem;
}

.label-chip {
    display: inline-block;
    padding: 6px 12px;
    margin-right: 8px;
    background-color: #eef2ff;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 600;
}

.priority-high { color: #dc2626; font-weight: 700; }
.priority-medium { color: #d97706; font-weight: 700; }
.priority-low { color: #16a34a; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown('<div class="main-title">🤖 AI-Powered GitHub Issue Assistant</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Instantly analyze, classify, and prioritize GitHub issues using AI</div>',
    unsafe_allow_html=True
)

st.write("")
 # Developer-friendly UI with copyable JSON and readable summaries
# -------------------------------------------------
# Input Card
# -------------------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🔍 Analyze a GitHub Issue")

repo_url = st.text_input(
    "GitHub Repository URL",
    placeholder="https://github.com/facebook/react"
)

issue_number = st.number_input(
    "Issue Number",
    min_value=1,
    step=1
)

analyze_btn = st.button("🚀 Analyze Issue", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# API Call & Output
# -------------------------------------------------
if analyze_btn:
    if not repo_url:
        st.warning("Please enter a valid GitHub repository URL.")
    else:
        with st.spinner("Analyzing issue using AI..."):
            try:
                BACKEND_API_KEY = os.getenv("BACKEND_API_KEY")

                response = requests.get(
                    "http://127.0.0.1:8000/analyze",
                    params={
                        "repo_url": repo_url,
                        "issue_number": issue_number
                    },
                    headers={
                        "x-api-key": BACKEND_API_KEY
                    },
                    timeout=120
                )

                if response.status_code == 200:
                    data = response.json()

                    # -----------------------------
                    # Human Readable Card
                    # -----------------------------
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.subheader("🧠 AI Analysis Summary")

                    st.markdown("**📌 Summary**")
                    st.write(data["summary"])

                    st.markdown("**🏷️ Issue Type**")
                    st.write(data["type"].capitalize())

                    st.markdown("**🚦 Priority**")
                    priority = data["priority_score"]

                    if priority >= 4:
                        st.markdown(f'<span class="priority-high">Priority {priority}</span>', unsafe_allow_html=True)
                    elif priority == 3:
                        st.markdown(f'<span class="priority-medium">Priority {priority}</span>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<span class="priority-low">Priority {priority}</span>', unsafe_allow_html=True)

                    st.markdown("**⚠️ Potential Impact**")
                    st.write(data["potential_impact"])

                    st.markdown("**🔖 Suggested Labels**")
                    for label in data["suggested_labels"]:
                        st.markdown(f'<span class="label-chip">{label}</span>', unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)

                    # -----------------------------
                    # Developer JSON Card
                    # -----------------------------
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.subheader("📦 Raw JSON Output (Developer View)")

                    formatted_json = json.dumps(data, indent=2)
                    st.code(formatted_json, language="json")

                    st.download_button(
                        label="📋 Copy JSON",
                        data=formatted_json,
                        file_name="issue_analysis.json",
                        mime="application/json"
                    )

                    st.markdown('</div>', unsafe_allow_html=True)

                else:
                    st.error(response.text)

            except Exception as e:
                st.error(f"Error connecting to backend: {e}")
