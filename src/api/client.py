"""
Async API client built on httpx.

This wraps:
- Base URL and default timeout
- Optional Authorization header
- Logging of requests and responses

Tests should usually call the service layer (services.py), but can
use this client directly for low-level negative / edge tests.
"""

from __future__ import annotations

import httpx

from config.settings import settings
from src.utils.logger import get_logger

logger = get_logger("api-client")


class ApiClient:
    """Thin async wrapper around httpx.AsyncClient for our test framework."""

    def __init__(self, base_url: str | None = None, token: str | None = None):
        self.base_url = base_url or settings.base_url
        self.token = token or settings.auth_token

        # AsyncClient supports concurrency and modern timeouts.
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=settings.api_timeout,
        )

    def _headers(self, auth: bool = True) -> dict[str, str]:
        """Build headers, optionally including Authorization."""
        headers = {"Content-Type": "application/json"}
        if auth and self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    async def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        await self._client.aclose()

    async def post(self, path: str, json: dict, auth: bool = True) -> httpx.Response:
        """POST JSON to path and log both request and response."""
        logger.info("POST %s body=%s", path, json)
        resp = await self._client.post(path, json=json, headers=self._headers(auth))
        logger.info("=> %s %s", resp.status_code, resp.text)
        return resp

    async def get(self, path: str, auth: bool = True) -> httpx.Response:
        """GET from path and log the call."""
        logger.info("GET %s", path)
        resp = await self._client.get(path, headers=self._headers(auth))
        logger.info("=> %s %s", resp.status_code, resp.text)
        return resp
