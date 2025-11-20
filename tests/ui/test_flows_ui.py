"""
UI tests built on pytest-playwright.

These tests consume reusable flows from src/ui/flows.py, which keeps
them short and maintainable.
"""

import pytest
import allure

from src.ui.flows import register_user, create_transaction_ui


@pytest.mark.ui
@allure.feature("User registration flow")
def test_user_registration_happy_path(page):
    """Happy-path: register a new premium user via the UI."""
    register_user(page, "John Doe", "john@example.com", "premium")

    success = page.get_by_text("User created successfully")
    success.wait_for()
    assert success.is_visible()


@pytest.mark.ui
@pytest.mark.negative
@allure.feature("User registration flow")
def test_user_regi
