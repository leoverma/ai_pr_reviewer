import time, os
import jwt
import httpx
from dotenv import load_dotenv

load_dotenv()
GITHUB_APP_ID = os.getenv("APP_ID")
GITHUB_PRIVATE_KEY_PATH = os.getenv("PRIVATE_KEY_PATH")  # path to downloaded .pem

def make_jwt():
    now = int(time.time())
    with open(GITHUB_PRIVATE_KEY_PATH, "rb") as f:
        private_pem = f.read()
    payload = {"iat": now - 60, "exp": now + (9*60), "iss": int(GITHUB_APP_ID)}
    token = jwt.encode(payload, private_pem, algorithm="RS256")
    return token

async def get_installation_token(installation_id: int) -> str:
    jwt_token = make_jwt()
    headers = {"Authorization": f"Bearer {jwt_token}", "Accept": "application/vnd.github+json"}
    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(url, headers=headers)
        r.raise_for_status()
        return r.json()["token"]
