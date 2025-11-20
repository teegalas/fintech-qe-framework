"""
Global pytest configuration and fixtures.

Key ideas:
- Provide a shared event loop for pytest-asyncio.
- Provide a session-scoped ApiClient.
- Provide service-layer fixtures (UsersService, TransactionsService).
- Provide reusable "user" and "transaction" fixtures.
- Capture Playwright screenshots into Allure on UI test failures.
"""

import asyncio

import allure
import pytest

from src.api.client import ApiClient
from src.api.services import UsersService, TransactionsService
from src.utils.data_factory import make_user, make_transaction


@pytest.fixture(scope="session")
def event_loop():
    """
    Override pytest-asyncio's default loop fixture to allow session scope.

    This lets us keep the ApiClient alive for the whole session.
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def api_client():
    """Session-scoped ApiClient shared across tests."""
    client = ApiClient()
    yield client
    await client.close()


@pytest.fixture(scope="session")
def users_service(api_client) -> UsersService:
    """High-level Users service for tests."""
    return UsersService(api_client)


@pytest.fixture(scope="session")
def transactions_service(api_client) -> TransactionsService:
    """High-level Transactions service for tests."""
    return TransactionsService(api_client)


@pytest.fixture
@pytest.mark.asyncio
async def user(users_service: UsersService):
    """
    Create a fresh random user for a test.

    Tests that need a valid user can simply depend on this fixture.
    """
    payload = make_user()
    return await users_service.create_user(payload)


@pytest.fixture
@pytest.mark.asyncio
async def transaction(user, transactions_service: TransactionsService):
    """
    Create a fresh random transaction for a given user.

    Useful for tests that require a pre-existing transaction.
    """
    payload = make_transaction(user_id=user.id)
    return await transactions_service.create_transaction(payload)


# Hook into test reporting to attach Playwright screenshots on UI failures.
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    If a test using the 'page' fixture fails at the 'call' phase,
    capture a screenshot and attach it to the Allure report.
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed and "page" in item.fixturenames:
        page = item.funcargs["page"]
        screenshot_bytes = page.screenshot(full_page=True)
        allure.attach(
            screenshot_bytes,
            name=f"{item.name}_screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
