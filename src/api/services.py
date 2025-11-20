"""
Service layer on top of ApiClient.

This is where we implement reusable, high-level flows that tests can call:
- create_user()
- get_user()
- create_transaction()
- list_for_user()

Using services keeps tests DRY and focused on validation instead of wiring.
"""

from __future__ import annotations
from typing import Sequence

from src.api.client import ApiClient
from src.api import routes
from src.utils.models import (
    UserCreate,
    User,
    TransactionCreate,
    Transaction,
)


class UsersService:
    """High-level operations for the Users domain."""

    def __init__(self, client: ApiClient):
        self.client = client

    async def create_user(self, payload: UserCreate) -> User:
        """Create a user and return the typed User model."""
        resp = await self.client.post(routes.USERS, json=payload.model_dump())
        resp.raise_for_status()
        return User.model_validate(resp.json())

    async def get_user(self, user_id: str) -> User:
        """Fetch a user by id and validate the response schema."""
        resp = await self.client.get(routes.user_by_id(user_id))
        resp.raise_for_status()
        return User.model_validate(resp.json())


class TransactionsService:
    """High-level operations for the Transactions domain."""

    def __init__(self, client: ApiClient):
        self.client = client

    async def create_transaction(self, payload: TransactionCreate) -> Transaction:
        """Create a transaction and return the typed Transaction model."""
        resp = await self.client.post(routes.TRANSACTIONS, json=payload.model_dump())
        resp.raise_for_status()
        return Transaction.model_validate(resp.json())

    async def list_for_user(self, user_id: str) -> Sequence[Transaction]:
        """List all transactions for a given user."""
        resp = await self.client.get(routes.transactions_by_user(user_id))
        resp.raise_for_status()
        data = resp.json()
        return [Transaction.model_validate(item) for item in data]
