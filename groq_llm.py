import os, httpx

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "mixtral-8x7b"

async def run_ai_review(diff_text: str):
    prompt = f"Review this Swift diff and list issues:\n{diff_text}"
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": "You are an expert Swift code reviewer."},
                    {"role": "user", "content": prompt}
                ]
            }
        )
        return r.json()["choices"][0]["message"]["content"]
