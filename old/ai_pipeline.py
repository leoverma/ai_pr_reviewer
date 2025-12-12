import asyncio
from utils.chunker import chunk_diff

async def mock_llm_review(prompt: str):
    # Replace this with OpenAI/other provider call in production
    await asyncio.sleep(0.2)
    # Simple heuristic: if file contains '!' (force unwrap), flag it
    if '!' in prompt and 'print' not in prompt:
        return [
            {
                "issue_type": "bug",
                "file": None,
                "line": 1,
                "severity": "high",
                "title": "Force unwrap risk",
                "details": "Force unwrap (`!`) can crash at runtime. Prefer safe unwrapping.",
                "suggested_fix": "Use `guard let` or `do/catch`."
            }
        ]
    return {"status": "clean"}

async def review_diff(diff_text: str):
    chunks = chunk_diff(diff_text, max_lines=80)
    results = []
    for c in chunks:
        llm_out = await mock_llm_review(c)
        if isinstance(llm_out, dict) and llm_out.get("status") == "clean":
            continue
        if isinstance(llm_out, list):
            results.extend(llm_out)
    if not results:
        return {"status": "clean"}
    return {"status": "issues_found", "issues": results)
