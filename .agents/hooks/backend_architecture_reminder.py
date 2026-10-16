"""Backend Architecture Reminder Hook (PreInvocation) with Path Filtering.

Path Filter: backend/**/*
Inspects conversation transcript and workspace state to only inject when backend files or tasks are active.
"""

import json
import os
import re
import sys

BACKEND_KEYWORDS = [
    r"\bbackend\b",
    r"\bapp/",
    r"\.py\b",
    r"\bfastapi\b",
    r"\bpydantic\b",
    r"\bpytest\b",
    r"\bruff\b",
    r"\bmypy\b",
    r"\buvicorn\b",
    r"\bjson_store\b",
    r"\brepositor(?:y|ies)\b",
]


def read_stdin() -> dict:
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def is_backend_active(data: dict) -> bool:
    transcript_path = data.get("transcriptPath")
    if transcript_path and os.path.exists(transcript_path):
        try:
            # Read last 30KB of transcript for recent user and tool messages
            with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
                f.seek(0, os.SEEK_END)
                size = f.tell()
                f.seek(max(0, size - 30000))
                recent_lines = f.readlines()[-25:]
                recent_text = "".join(recent_lines)
                for pattern in BACKEND_KEYWORDS:
                    if re.search(pattern, recent_text, re.IGNORECASE):
                        return True
        except Exception:
            pass

    # Default fallback: check if CWD or arguments relate to backend
    return False


def main() -> None:
    data = read_stdin()

    if not is_backend_active(data):
        sys.stdout.write(json.dumps({"injectSteps": []}))
        return

    response = {
        "injectSteps": [
            {
                "ephemeralMessage": (
                    "[Backend Architecture Guard] "
                    "1) Follow strict 5-layer architecture: types -> models -> repositories -> services -> routers. "
                    "2) Multi-tenancy: always filter and scope records by current_user.id. "
                    "3) Never edit backend/data/*.json directly; use repositories. "
                    "4) Validate changes with 'uv run ruff format --check .', 'uv run ruff check .', "
                    "'uv run mypy app', and 'uv run pytest'."
                )
            }
        ]
    }
    sys.stdout.write(json.dumps(response))


if __name__ == "__main__":
    main()
