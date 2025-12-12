from diff_parser import fetch_and_extract_swift_diff
from groq_llm import run_ai_review

async def process_review(diff_url):
    diff = await fetch_and_extract_swift_diff(diff_url)
    if not diff:
        return ["No Swift files detected"]
    result = await run_ai_review(diff)
    return result
