import os, httpx, jwt, time

APP_ID = os.getenv("GITHUB_APP_ID")
PRIVATE_KEY = os.getenv("GITHUB_PRIVATE_KEY")

def make_jwt():
    now = int(time.time())
    payload = {"iat": now-60, "exp": now+540, "iss": APP_ID}
    return jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")

async def post_pr_comment(repo, number, body):
    token = make_jwt()
    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://api.github.com/repos/{repo}/issues/{number}/comments",
            headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
            json={"body": body},
        )
