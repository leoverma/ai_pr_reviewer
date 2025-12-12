import httpx

async def download_diff(diff_url: str, installation_token: str) -> str:
    headers = {
        "Authorization": f"token {installation_token}",
        "Accept": "application/vnd.github.v3.diff"
    }
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(diff_url, headers=headers)
        r.raise_for_status()
        return r.text
