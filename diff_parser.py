import re
from typing import List, Dict

FILE_HDR_RE = re.compile(r"^diff --git a/(.+) b/(.+)$")

def parse_diff(diff_text: str) -> List[Dict]:
    lines = diff_text.splitlines()
    files = []
    current = None
    for line in lines:
        m = FILE_HDR_RE.match(line)
        if m:
            if current:
                files.append(current)
            current = {"old": m.group(1), "new": m.group(2), "raw": []}
            continue
        if current is None:
            continue
        current["raw"].append(line)
    if current:
        files.append(current)

    swift_files = []
    for f in files:
        filename = f["new"]
        if filename.endswith(".swift"):
            diff_for_file = "\n".join(f["raw"])
            swift_files.append({"file_path": filename, "diff": diff_for_file})
    return swift_files
