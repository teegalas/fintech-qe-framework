"""
Validation-focused tests for Transactions.

We use parametrization to cover multiple invalid amounts in a single test
(Do Not Repeat Yourself).
"""

import pytest

from src.utils.data_factory import make_transaction
from src.api import routes


@pytest.mark.asyncio
@pytest.mark.negative
@pytest.mark.parametrize(
    "amount",
    [-1, -0.01, 0],
    ids=lambda v: f"amount_{v}",
)
async def test_create_transaction_invalid_amounts(api_client, user, amount):
    """
    Negative: amounts that should be rejected by the API.

    Adjust the expected status codes depending on your implementation (400/422).
    """
    payload = make_transaction(user_id=user.id).model_dump()
    payload["amount"] = amount

    resp = await api_client.post(routes.TRANSACTIONS, json=payload)
    assert resp.status_code in (400, 422)
