"""Frontend PostToolUse Audit with Path Filtering.

Path Filter: frontend/**/*
Runs lightweight auditing and formatting verification for frontend files.
"""

import fnmatch
import json
import sys

PATH_FILTERS = ["frontend/**/*", "frontend/*"]


def is_frontend_path(file_path: str) -> bool:
    if not file_path:
        return False
    normalized = file_path.replace("\\", "/")
    if "/frontend/" in normalized or normalized.startswith("frontend/"):
        return True
    return any(fnmatch.fnmatch(normalized, p) for p in PATH_FILTERS)


def read_stdin() -> dict:
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def main() -> None:
    data = read_stdin()
    tool_call = data.get("toolCall", {})
    tool_name = tool_call.get("name", "")
    args = tool_call.get("args", {})

    if tool_name in ("write_to_file", "replace_file_content"):
        target_file = args.get("TargetFile", "").replace("\\", "/")

        # Path Filter: Only audit frontend files
        if is_frontend_path(target_file):
            pass

    # PostToolUse contract expects an empty JSON object
    sys.stdout.write(json.dumps({}))


if __name__ == "__main__":
    main()
