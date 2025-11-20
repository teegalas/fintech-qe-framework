"""
Domain models for the fintech-like API under test, based on pydantic v2.

These models:
- Provide type-safety in your tests
- Validate API responses
- Define a single source of truth for data shape
"""

from typing import Literal

from pydantic import BaseModel, EmailStr, field_validator

AccountType = Literal["basic", "premium", "business"]
TxType = Literal["transfer", "deposit", "withdrawal"]


class UserCreate(BaseModel):
    """Payload for creating a user via the API."""
    name: str
    email: EmailStr
    accountType: AccountType


class User(BaseModel):
    """User as returned from the API."""
    id: str
    name: str
    email: EmailStr
    accountType: AccountType


class TransactionCreate(BaseModel):
    """Payload for creating a transaction via the API."""
    userId: str
    amount: float
    type: TxType
    recipientId: str
    reference: str


class Transaction(BaseModel):
    """Transaction as returned from the API."""
    id: str
    userId: str
    amount: float
    type: TxType
    recipientId: str
    reference: str

    @field_validator("amount")
    @classmethod
    def amount_must_be_non_negative(cls, v: float) -> float:
        """Guard against negative amounts in API responses."""
        assert v >= 0, "Amount must be non-negative"
        return v
