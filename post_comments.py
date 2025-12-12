import httpx
import textwrap
from typing import List, Dict

async def post_summary_comment(owner: str, repo: str, pr_number: int, token: str, issues: List[Dict]):
    body = build_summary_md(issues)
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
    async with httpx.AsyncClient() as client:
        r = await client.post(url, json={"body": body}, headers=headers)
        r.raise_for_status()
        return r.json()

def build_summary_md(issues: List[Dict]) -> str:
    if not issues:
        return "✅ SwiftReview AI: No issues found."
    lines = ["## ⚠️ SwiftReview AI — Automated Review Summary", "", f"**Total issues**: {len(issues)}", ""]
    grouped = {}
    for i in issues:
        k = i.get("issue_type", "other")
        grouped.setdefault(k, []).append(i)
    for k, v in grouped.items():
        lines.append(f"### {k.title()} ({len(v)})")
        for iss in v[:20]:
            file = iss.get("file") or "unknown"
            title = iss.get("title")
            sev = iss.get("severity")
            details = iss.get("details", "")
            suggestion = iss.get("suggested_fix", "")
            lines.append(f"- **{title}** — `{file}` — *{sev}*")
            if details:
                lines.append(f"  - {textwrap.shorten(details, width=200)}")
            if suggestion:
                lines.append(f"  - **Suggestion:** {textwrap.shorten(suggestion, width=200)}")
        lines.append("")
    lines.append("---")
    lines.append("Powered by SwiftReview AI")
    return "\n".join(lines)

async def post_file_comments(owner: str, repo: str, pr_number: int, token: str, issues: List[Dict]):
    per_file = {}
    for i in issues:
        file = i.get("file", "unknown")
        per_file.setdefault(file, []).append(i)
    results = []
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
    async with httpx.AsyncClient() as client:
        for file, items in per_file.items():
            body_lines = [f"**Automated suggestions for `{file}`**", ""]
            for iss in items:
                body_lines.append(f"- **{iss.get('title')}** — *{iss.get('severity')}*")
                if iss.get("details"):
                    body_lines.append(f"  - {iss.get('details')}")
                if iss.get("suggested_fix"):
                    body_lines.append(f"  - **Fix:**\n\n```swift\n{iss.get('suggested_fix')}\n```")
                body_lines.append("")
            payload = {"body": "\n".join(body_lines)}
            url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
            r = await client.post(url, json=payload, headers=headers)
            r.raise_for_status()
            results.append(r.json())
    return results
