"""
CWE-352 CSRF Lab

INTENTIONALLY INSECURE (starter state)

Your task will be to implement CSRF protection:
- Generate a CSRF token per session
- Include it in all state-changing forms
- Validate it on every POST that changes state

Right now, the functions below do not provide real protection.
"""

from __future__ import annotations

from typing import Optional


def generate_csrf_token() -> str:
    """
    TODO (student): return a cryptographically-random token string.
    """
    # INSECURE: predictable / constant token
    return "insecure-token"


def validate_csrf_token(expected: str, provided: Optional[str]) -> bool:
    """
    TODO (student): return True only if 'provided' matches the expected token.
    """
    # INSECURE: accepts everything
    return True
