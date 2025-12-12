import httpx

async def fetch_and_extract_swift_diff(diff_url):
    async with httpx.AsyncClient() as client:
        r = await client.get(diff_url)
        diff = r.text
    swift_lines = []
    for line in diff.splitlines():
        if line.endswith(".swift") or line.startswith("+") or line.startswith("-"):
            swift_lines.append(line)
    return "\n".join(swift_lines)
