"""
API tests for the Users domain.

These tests:
- Use the UsersService for happy-path flows
- Use the raw ApiClient for negative tests when necessary
"""

import pytest
import allure

from src.utils.data_factory import make_user
from src.utils.models import User
from src.api import routes


@pytest.mark.asyncio
@allure.feature("Users")
@allure.story("Create user")
async def test_create_user_success(users_service: "UsersService"):
    """Happy-path: create a premium user."""
    payload = make_user(account_type="premium")

    user: User = await users_service.create_user(payload)

    assert user.email == payload.email
    assert user.accountType == "premium"


@pytest.mark.asyncio
@allure.feature("Users")
@allure.story("Get user by id")
async def test_get_user_by_id(users_service: "UsersService", user: User):
    """Happy-path: fetch a user we just created."""
    fetched = await users_service.get_user(user.id)
    assert fetched.id == user.id
    assert fetched.email == user.email


@pytest.mark.asyncio
@pytest.mark.negative
@allure.feature("Users")
@allure.story("Validation errors")
async def test_create_user_missing_email_returns_client_error(api_client):
    """
    Negative: omit the 'email' field and expect a 4xx error.

    We call the low-level client directly here so we can send
    intentionally invalid payloads.
    """
    payload = make_user().model_dump()
    payload.pop("email")

    resp = await api_client.post(routes.USERS, json=payload)
    assert resp.status_code in (400, 422)
