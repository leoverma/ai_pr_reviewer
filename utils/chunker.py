def chunk_diff(diff_text: str, max_lines: int = 80):
    lines = diff_text.splitlines()
    chunks = []
    cur = []
    for ln in lines:
        cur.append(ln)
        if len(cur) >= max_lines:
            chunks.append("\n".join(cur))
            cur = []
    if cur:
        chunks.append("\n".join(cur))
    return chunks
