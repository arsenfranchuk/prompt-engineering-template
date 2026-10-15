import hashlib
import secrets


def hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    """Hashes a password using PBKDF2-HMAC-SHA256 with a cryptographic salt."""
    if salt is None:
        salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        iterations=100_000,
    ).hex()
    return hashed, salt


def verify_password(password: str, password_hash: str, salt: str) -> bool:
    """Verifies that a plain text password matches the stored hash and salt."""
    new_hash, _ = hash_password(password, salt)
    return secrets.compare_digest(new_hash, password_hash)


def generate_session_token() -> str:
    """Generates a secure random session token."""
    return secrets.token_hex(32)
