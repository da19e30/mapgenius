"""
Authentication service module.

This module re-exports the authentication functions from jwt.py
to maintain backward compatibility with import statements that expect
app.services.auth.

All actual implementations (hash_password, verify_password, create_access_token, etc.)
are in app.services.jwt.
"""

from .jwt import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    decode_token,
)

__all__ = [
    "hash_password",
    "verify_password",
    "create_access_token",
    "get_current_user",
    "decode_token",
]
