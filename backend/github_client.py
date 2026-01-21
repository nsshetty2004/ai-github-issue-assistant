import requests

def fetch_issue(repo_url: str, issue_number: int):
    repo_url = repo_url.strip()  # ✅ CRITICAL FIX

    if not repo_url.startswith("https://github.com/"):
        raise ValueError("Invalid GitHub repository URL")

    owner_repo = repo_url.replace("https://github.com/", "")
    owner, repo = owner_repo.split("/")

    issue_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-issue-ai"
    }

    response = requests.get(issue_url, headers=headers)
    response.raise_for_status()
    issue = response.json()

    comments = []
    if issue.get("comments", 0) > 0:
        comments_resp = requests.get(issue["comments_url"], headers=headers)
        comments_resp.raise_for_status()
        comments = comments_resp.json()

    return {
        "title": issue.get("title", ""),
        "body": issue.get("body") or "",
        "comments": [c.get("body", "") for c in comments]
    }
