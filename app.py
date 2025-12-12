from fastapi import FastAPI, Request
from mangum import Mangum
from event_handler import handle_event

app = FastAPI()

@app.post("/webhook/github")
async def github_webhook(request: Request):
    payload = await request.json()
    await handle_event(payload)
    return {"status": "ok"}

handler = Mangum(app)
