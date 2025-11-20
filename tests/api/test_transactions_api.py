"""
API tests for the Transactions domain.

These tests exercise happy-path flows via the TransactionsService
and use fixtures to avoid repeating user / transaction setup.
"""

import pytest
import allure

from src.utils.data_factory import make_transaction
from src.utils.models import Transaction


@pytest.mark.asyncio
@allure.feature("Transactions")
@allure.story("Create transaction")
async def test_create_transaction_success(user, transactions_service: "TransactionsService"):
    """Happy-path: create a transaction for a user."""
    payload = make_transaction(user_id=user.id)

    tx: Transaction = await transactions_service.create_transaction(payload)

    assert tx.userId == user.id
    assert tx.amount == payload.amount
    assert tx.type == payload.type


@pytest.mark.asyncio
@allure.feature("Transactions")
@allure.story("List user transactions")
async def test_list_transactions_for_user(user, transactions_service: "TransactionsService"):
    """Happy-path: list transactions for a user after creating some."""
    # Arrange: create a couple of transactions for this user.
    for _ in range(2):
        await transactions_service.create_transaction(make_transaction(user_id=user.id))

    txs = await transactions_service.list_for_user(user.id)

    assert len(txs) >= 2
    # All returned transactions should belong to the same user.
    assert {t.userId for t in txs} == {user.id}
