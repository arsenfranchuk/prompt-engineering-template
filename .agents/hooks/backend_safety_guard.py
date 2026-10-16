"""Backend PreToolUse Safety Guard with Path Filtering.

Path Filter: backend/**/*
Protects backend entity JSON storage, uv.lock, and blocks destructive commands.
"""

import fnmatch
import json
import re
import sys

PATH_FILTERS = ["backend/**/*", "backend/*"]


def is_backend_path(file_path: str) -> bool:
    if not file_path:
        return False
    normalized = file_path.replace("\\", "/")
    # Direct check or glob match
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

    # 1. Run Command Checks
    if tool_name == "run_command":
        cmd = args.get("CommandLine", "").strip()
        cwd = args.get("Cwd", "").replace("\\", "/")

        # Global destructive commands are always blocked regardless of path
        destructive_patterns = [
            r"\brm\s+-(?:r[fv]|f[rv]|rf)\b",
            r"\bdel\s+/[fq]\s+/[fq]\b",
            r"\brmdir\s+/s\s+/q\b",
            r"Remove-Item\s+.*-Recurse\s+.*-Force",
            r"\bgit\s+reset\s+--hard\b",
            r"\bgit\s+clean\s+-(?:f[dx]|d[fx]|fdx)\b",
            r"\bgit\s+push\s+.*--force\b",
            r"\bdrop\s+database\b",
            r"\btruncate\s+table\b",
        ]
        for pattern in destructive_patterns:
            if re.search(pattern, cmd, re.IGNORECASE):
                sys.stdout.write(
                    json.dumps(
                        {
                            "decision": "deny",
                            "reason": f"[Backend Safety Guard] Destructive command blocked: {cmd}",
                        }
                    )
                )
                return

    # 2. File Modification Checks (Path Filtered to backend/**/*)
    if tool_name in ("write_to_file", "replace_file_content"):
        target_file = args.get("TargetFile", "").replace("\\", "/")

        # Path Filter: only apply backend guard if the file is within backend/
        if not is_backend_path(target_file):
            sys.stdout.write(json.dumps({"decision": "allow"}))
            return

        content = args.get("CodeContent", "") + args.get("ReplacementContent", "")

        # Direct edits to persistent JSON entity files in backend/data/
        if re.search(r"backend/data/.*\.json$", target_file, re.IGNORECASE):
            sys.stdout.write(
                json.dumps(
                    {
                        "decision": "deny",
                        "reason": f"[Backend Safety Guard] Direct editing of persistent JSON data store ({target_file}) is prohibited. All updates must go through Repository and Service layers.",
                    }
                )
            )
            return

        # Lockfile manual tampering
        if re.search(r"(?:^|/)uv\.lock$", target_file, re.IGNORECASE):
            sys.stdout.write(
                json.dumps(
                    {
                        "decision": "ask",
                        "reason": f"[Backend Safety Guard] Manual editing of 'uv.lock' detected. Lockfiles should be generated via 'uv sync'. Proceed with manual edit?",
                    }
                )
            )
            return

        # Hardcoded backend secrets
        secret_patterns = [
            r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
            r"\bghp_[a-zA-Z0-9]{36}\b",
            r"\bAIza[0-9A-Za-z-_]{35}\b",
            r"\bAKIA[0-9A-Z]{16}\b",
        ]
        for pattern in secret_patterns:
            if re.search(pattern, content):
                sys.stdout.write(
                    json.dumps(
                        {
                            "decision": "deny",
                            "reason": f"[Backend Safety Guard] Hardcoded secret detected in {target_file}. Use environment variables instead.",
                        }
                    )
                )
                return

        # Router auth bypass check
        if "backend/app/routers/" in target_file:
            if "bypass_auth = True" in content or "# skipcq: auth" in content:
                sys.stdout.write(
                    json.dumps(
                        {
                            "decision": "deny",
                            "reason": f"[Backend Safety Guard] Insecure authentication bypass pattern detected in router {target_file}.",
                        }
                    )
                )
                return

    sys.stdout.write(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    main()
