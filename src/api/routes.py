"""
Central definitions for API routes.

Using helper functions is more DRY than hardcoding the same string
pattern in every test.
"""

USERS = "/api/users"
TRANSACTIONS = "/api/transactions"


def user_by_id(user_id: str) -> str:
    """Return the URL path for a specific user."""
    return f"{USERS}/{user_id}"


def transactions_by_user(user_id: str) -> str:
    """Return the URL path for listing transactions for a user."""
    return f"{TRANSACTIONS}/{user_id}"
