"""Frontend PreToolUse Safety Guard with Path Filtering.

Path Filter: frontend/**/*
Protects frontend package-lock.json, prevents client-side secret leaks and destructive actions.
"""

import fnmatch
import json
import re
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

    # 1. Run Command Checks
    if tool_name == "run_command":
        cmd = args.get("CommandLine", "").strip()
        if re.search(
            r"\b(?:rm\s+-rf\s+node_modules|Remove-Item\s+.*node_modules\s+.*-Recurse)\b",
            cmd,
            re.IGNORECASE,
        ):
            sys.stdout.write(
                json.dumps(
                    {
                        "decision": "ask",
                        "reason": f"[Frontend Safety Guard] Deletion of 'node_modules' detected. Reinstallation will take time. Confirm: {cmd}",
                    }
                )
            )
            return

    # 2. File Modification Checks (Path Filtered to frontend/**/*)
    if tool_name in ("write_to_file", "replace_file_content"):
        target_file = args.get("TargetFile", "").replace("\\", "/")

        # Path Filter: only apply frontend guard if the file is within frontend/
        if not is_frontend_path(target_file):
            sys.stdout.write(json.dumps({"decision": "allow"}))
            return

        content = args.get("CodeContent", "") + args.get("ReplacementContent", "")

        # Lockfile manual edit guard
        if re.search(r"(?:^|/)package-lock\.json$", target_file, re.IGNORECASE):
            sys.stdout.write(
                json.dumps(
                    {
                        "decision": "ask",
                        "reason": f"[Frontend Safety Guard] Manual editing of 'package-lock.json' detected. Use 'npm install' instead. Proceed?",
                    }
                )
            )
            return

        # Client-side secrets leak
        if "frontend/src/" in target_file:
            client_secret_patterns = [
                r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----",
                r"\bghp_[a-zA-Z0-9]{36}\b",
                r"\bAIza[0-9A-Za-z-_]{35}\b",
                r"\bAKIA[0-9A-Z]{16}\b",
            ]
            for pattern in client_secret_patterns:
                if re.search(pattern, content):
                    sys.stdout.write(
                        json.dumps(
                            {
                                "decision": "deny",
                                "reason": f"[Frontend Safety Guard] Hardcoded secret or private credential detected in client code ({target_file}). Use environment variables or backend proxies.",
                            }
                        )
                    )
                    return

    sys.stdout.write(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    main()
