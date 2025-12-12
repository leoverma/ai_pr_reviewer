import os
import asyncio
import hmac
import hashlib
from fastapi import FastAPI, Request, Header, HTTPException
from worker import enqueue_job, start_background_worker
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")  # set in .env

def verify_signature(body: bytes, signature_header: str) -> bool:
    if not signature_header:
        return False
    try:
        sha_name, sig = signature_header.split("=")
    except ValueError:
        return False
    if sha_name != "sha256":
        return False
    mac = hmac.new(WEBHOOK_SECRET.encode(), msg=body, digestmod=hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), sig)

@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_event_loop()
    start_background_worker(loop)

@app.post("/webhook/github")
async def github_webhook(request: Request, x_hub_signature_256: str = Header(None), x_github_event: str = Header(None)):
    raw = await request.body()
    if not verify_signature(raw, x_hub_signature_256):
        raise HTTPException(status_code=401, detail="Invalid signature")
    payload = await request.json()
    event = x_github_event

    # We only care about PR events (opened, synchronize, reopened, edited)
    if event == "pull_request" and payload.get("action") in ["opened", "synchronize", "reopened", "edited"]:
        pr = payload["pull_request"]
        repo_full = payload["repository"]["full_name"]
        diff_url = pr.get("diff_url") or pr.get("patch_url")
        installation = payload.get("installation", {})
        installation_id = installation.get("id")
        job = {
            "repo": repo_full,
            "pr_number": pr["number"],
            "diff_url": diff_url,
            "title": pr.get("title", ""),
            "author": pr.get("user", {}).get("login", ""),
            "installation_id": installation_id,
            "head_sha": pr.get("head", {}).get("sha")
        }
        await enqueue_job(job)
        return {"status": "accepted"}
    return {"status": "ignored"}
