"""
Reusable UI flows for Playwright tests.

These functions encapsulate common journeys so tests stay small and readable.
If the UI changes (labels/selectors), update them here once.
"""

from playwright.sync_api import Page


def register_user(page: Page, name: str, email: str, account_type: str = "basic") -> None:
    """Fill and submit the user registration form."""
    page.goto("/register")
    page.get_by_label("Name").fill(name)
    page.get_by_label("Email").fill(email)
    page.get_by_label("Account type").select_option(account_type)
    page.get_by_role("button", name="Sign up").click()


def create_transaction_ui(
    page: Page,
    user_id: str,
    amount: float,
    tx_type: str,
    recipient_id: str,
) -> None:
    """Fill and submit the transaction creation form."""
    page.goto("/transactions/new")
    page.get_by_label("User ID").fill(user_id)
    page.get_by_label("Amount").fill(str(amount))
    page.get_by_label("Type").select_option(tx_type)
    page.get_by_label("Recipient ID").fill(recipient_id)
    page.get_by_role("button", name="Create transaction").click()
