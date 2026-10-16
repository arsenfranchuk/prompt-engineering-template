"""Backend PostToolUse Audit with Path Filtering.

Path Filter: backend/**/*
Runs lightweight auto-formatting (Ruff) on modified Python files in backend/.
"""

import fnmatch
import json
import os
import subprocess
import sys

PATH_FILTERS = ["backend/**/*", "backend/*"]


def is_backend_path(file_path: str) -> bool:
    if not file_path:
        return False
    normalized = file_path.replace("\\", "/")
    if "/backend/" in normalized or normalized.startswith("backend/"):
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

        # Path Filter: Only audit backend python files
        if is_backend_path(target_file) and target_file.endswith(".py"):
            project_root = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..")
            )
            backend_dir = os.path.join(project_root, "backend")
            try:
                subprocess.run(
                    ["uv", "run", "ruff", "format", target_file],
                    cwd=backend_dir,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=5,
                    check=False,
                )
            except Exception:
                pass

    # PostToolUse contract expects an empty JSON object
    sys.stdout.write(json.dumps({}))


if __name__ == "__main__":
    main()
