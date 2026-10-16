"""Frontend Architecture Reminder Hook (PreInvocation) with Path Filtering.

Path Filter: frontend/**/*
Inspects conversation transcript and workspace state to only inject when frontend files or tasks are active.
"""

import json
import os
import re
import sys

FRONTEND_KEYWORDS = [
    r"\bfrontend\b",
    r"\bsrc/",
    r"\.(?:tsx|jsx|ts)\b",
    r"\breact\b",
    r"\bredux\b",
    r"\brtk\b",
    r"\bshadcn\b",
    r"\btailwind\b",
    r"\bvite\b",
    r"\boxlint\b",
    r"\bprettier\b",
]


def read_stdin() -> dict:
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def is_frontend_active(data: dict) -> bool:
    transcript_path = data.get("transcriptPath")
    if transcript_path and os.path.exists(transcript_path):
        try:
            with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
                f.seek(0, os.SEEK_END)
                size = f.tell()
                f.seek(max(0, size - 30000))
                recent_lines = f.readlines()[-25:]
                recent_text = "".join(recent_lines)
                for pattern in FRONTEND_KEYWORDS:
                    if re.search(pattern, recent_text, re.IGNORECASE):
                        return True
        except Exception:
            pass

    return False


def main() -> None:
    data = read_stdin()

    if not is_frontend_active(data):
        sys.stdout.write(json.dumps({"injectSteps": []}))
        return

    response = {
        "injectSteps": [
            {
                "ephemeralMessage": (
                    "[Frontend Architecture Guard] "
                    "1) Feature-first structure: place UI and state under 'src/features/<feature>/'. "
                    "2) Use Redux Toolkit and RTK Query with tag-based cache invalidation. "
                    "3) UI components must use Tailwind CSS & shadcn/ui. "
                    "4) Validate changes with 'npm run lint', 'npm run format:check', and 'npm run typecheck'."
                )
            }
        ]
    }
    sys.stdout.write(json.dumps(response))


if __name__ == "__main__":
    main()
