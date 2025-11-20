"""
Data factories for test payloads.

The goal is to:
- Centralize randomization
- Keep tests readable (make_user(), make_transaction())
- Avoid duplicating payload construction in every test
"""

from __future__ import annotations

import random
import uuid
from datetime import datetime

from .models import (
    AccountType,
    TxType,
    UserCreate,
    TransactionCreate,
)

ACCOUNT_TYPES: list[AccountType] = ["basic", "premium", "business"]
TX_TYPES: list[TxType] = ["transfer", "deposit", "withdrawal"]


def random_email(prefix: str = "user") -> str:
    """Generate a unique-looking email address for tests."""
    return f"{prefix}_{uuid.uuid4().hex[:8]}@example.com"


def make_user(account_type: AccountType | None = None) -> UserCreate:
    """
    Build a valid user payload.

    account_type is optional; if omitted we pick one randomly.
    """
    return UserCreate(
        name=f"User {uuid.uuid4().hex[:4]}",
        email=random_email("fintech"),
        accountType=account_type or random.choice(ACCOUNT_TYPES),
    )


def make_transaction(user_id: str) -> TransactionCreate:
    """
    Build a valid transaction payload for the given user_id.

    We randomize amount, type and recipientId to avoid collisions.
    """
    return TransactionCreate(
        userId=user_id,
        amount=round(random.uniform(1, 500), 2),
        type=random.choice(TX_TYPES),
        recipientId=uuid.uuid4().hex[:6],
        reference=f"TX-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
    )
