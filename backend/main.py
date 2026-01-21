from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, Header
import os

from backend.github_client import fetch_issue
from backend.llm_analyzer import analyze_issue

app = FastAPI()

@app.get("/analyze")
def analyze(
    repo_url: str,
    issue_number: int,
    x_api_key: str = Header(None)
):
    if x_api_key != os.getenv("BACKEND_API_KEY"):
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        issue_data = fetch_issue(repo_url, issue_number)
        analysis = analyze_issue(issue_data)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
