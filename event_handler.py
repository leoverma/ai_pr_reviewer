from review_pipeline import process_review
from github_layer import post_pr_comment

async def handle_event(payload):
    if payload.get("action") not in ["opened","synchronize","reopened","edited"]:
        return
    pr = payload["pull_request"]
    repo = payload["repository"]["full_name"]
    number = pr["number"]
    diff_url = pr["diff_url"]
    issues = await process_review(diff_url)
    await post_pr_comment(repo, number, issues)
