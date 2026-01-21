AI-Powered GitHub Issue Assistant
Overview

This project is a lightweight AI-powered assistant that analyzes GitHub issues and generates structured, decision-ready insights for engineering teams.

Given a public GitHub repository URL and an issue number, the system:

fetches the issue context (title, description, comments),

analyzes it using an AI reasoning layer,

and returns a strictly structured JSON output containing issue type, priority, labels, and potential impact.

The goal of this project is to demonstrate agentic thinking, clean system design, and practical AI integration, rather than just calling an LLM.

Key Features

Fetches real GitHub issue data using the GitHub REST API

Analyzes issues using an AI reasoning layer

Enforces a strict JSON output contract

Handles AI failures gracefully using fallback logic

Simple, clean frontend for easy interaction

Designed to be reliable, testable, and demo-ready

Architecture
User (Browser)
   ↓
Streamlit Frontend
   ↓ (HTTP Request)
FastAPI Backend (/analyze)
   ├── GitHub API Client (fetch issue data)
   ├── AI Analyzer (LLM or fallback logic)
   └── Pydantic Schema Validation
   ↓
Structured JSON Response

Design Principles

Separation of concerns
GitHub data fetching, AI reasoning, and API orchestration are isolated.

Contract-first design
AI output is validated using Pydantic schemas to guarantee structure.

Reliability over fragility
The system never crashes or hangs due to AI failures.

Tech Stack

Backend: Python, FastAPI, Pydantic

Frontend: Streamlit

APIs: GitHub REST API

AI Layer: LLM-ready design with safe fallback logic

Project Structure
github-issue-ai/
│
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── github_client.py     # GitHub API integration
│   ├── llm_analyzer.py      # AI reasoning + fallback logic
│   ├── models.py            # Pydantic output schemas
│
├── frontend/
│   └── app.py               # Streamlit UI
│
├── requirements.txt
├── .env.example
├── README.md

Setup & Run (Under 5 Minutes)
1️⃣ Clone the Repository
git clone <your-repo-url>
cd github-issue-ai

2️⃣ Create a Virtual Environment (Recommended)
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

Run the Backend (FastAPI)
uvicorn backend.main:app --reload


Verify backend is running:

http://127.0.0.1:8000/docs

Run the Frontend (Streamlit)

Open a new terminal:

streamlit run frontend/app.py


Open in browser:

http://localhost:8501

Example Usage

Input

Repository URL: https://github.com/facebook/react

Issue Number: 1

Output (example)

{
  "summary": "Run each test in its own <iframe>",
  "type": "feature_request",
  "priority_score": 3,
  "suggested_labels": ["enhancement", "discussion"],
  "potential_impact": "Improves developer experience but does not block users."
}

AI & Fallback Strategy

The AI layer is designed to be provider-agnostic.

The system supports real LLM integration

When an LLM is unavailable or rate-limited:

a deterministic fallback analyzer is used

output still follows the required JSON schema

This ensures the system is:

reliable

demo-friendly

production-safe

Predictability and correctness were prioritized over best-effort generation.

Edge Cases Handled

Issues with no comments

Empty issue bodies

Invalid repository URLs or issue numbers

AI service failures or rate limits

Invalid AI outputs (schema validation enforced)

Design Decisions

Strict JSON schema for safe downstream consumption

Low coupling between AI logic and orchestration

Minimal UI focused on clarity and usability

Fallback-first mindset to reflect real-world AI systems

Future Improvements

Caching previously analyzed issues

GitHub OAuth for private repositories

Confidence scores for suggested labels

Streaming AI responses

Final Notes

This project is intentionally small but complete.
It focuses on real-world AI system design, emphasizing reliability, clarity, and developer experience rather than raw model usage.
This project emphasizes reliability, clarity, and production-ready AI design.

Author: Shashank N