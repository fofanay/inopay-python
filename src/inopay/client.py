"""Inopay Python SDK — synchronous client wrapping the public sandbox."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

import requests


@dataclass(frozen=True)
class Instrument:
    symbol: str
    name: str
    market: str  # 'BRVM' | 'BVMAC' | 'GSE'
    currency: str  # 'XOF' | 'XAF' | 'GHS'
    last_price: float
    change_pct: float


@dataclass(frozen=True)
class SGI:
    id: str
    name: str
    market: str
    fill_rate: float


@dataclass(frozen=True)
class Order:
    id: str
    symbol: str
    side: str  # 'buy' | 'sell'
    qty: int
    sgi_id: str
    status: str
    avg_price: float
    filled_qty: int
    filled_at: Optional[str] = None
    settlement_date: Optional[str] = None
    settlement_currency: Optional[str] = None


@dataclass(frozen=True)
class KycAttestation:
    schema: str
    user_id: str
    issuer: str
    level: str
    issued_at: str
    expires_at: str
    key_id: str
    ed25519_signature: str


class InopayError(Exception):
    """Raised on non-2xx responses from the Inopay API."""

    def __init__(self, status: int, code: str, detail: Optional[str] = None) -> None:
        super().__init__(f"InopayError({status} {code}): {detail or ''}")
        self.status = status
        self.code = code
        self.detail = detail


class InopayClient:
    """Inopay client — synchronous, requests-based.

    :param api_key: API key. Use ``sk_test_demo_inopay_2026`` for the public sandbox (60 req/min/IP).
    :param base_url: defaults to the public sandbox.
    :param timeout: HTTP timeout in seconds (default 30).
    :param session: optional pre-configured ``requests.Session`` (useful for tests, retries, proxies).
    """

    DEFAULT_BASE_URL = "https://api.getinopay.com/v1/sandbox"

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        session: Optional[requests.Session] = None,
    ) -> None:
        if not api_key:
            raise ValueError("InopayClient: api_key is required")
        self.api_key = api_key
        self.base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout
        self._session = session or requests.Session()

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        url = f"{self.base_url}/{path.lstrip('/')}"
        headers = kwargs.pop("headers", {}) or {}
        headers.setdefault("Authorization", f"Bearer {self.api_key}")
        headers.setdefault("Accept", "application/json")
        if "json" in kwargs:
            headers.setdefault("Content-Type", "application/json")
        resp = self._session.request(
            method, url, headers=headers, timeout=self.timeout, **kwargs
        )
        if not resp.ok:
            try:
                payload = resp.json()
            except Exception:
                payload = {}
            raise InopayError(
                status=resp.status_code,
                code=payload.get("error") or f"http_{resp.status_code}",
                detail=payload.get("detail") or resp.text[:300],
            )
        return resp.json()

    # ── Endpoints ───────────────────────────────────────────

    def health(self) -> dict:
        """Sandbox status."""
        return self._request("GET", "/health")

    def instruments_list(self) -> dict:
        """List BRVM / BVMAC / GSE instruments."""
        return self._request("GET", "/instruments")

    def sgis_list(self) -> dict:
        """List partner SGIs available in the sandbox."""
        return self._request("GET", "/sgis")

    def order_create(
        self,
        symbol: str,
        side: str,
        qty: int,
        sgi_id: Optional[str] = None,
    ) -> dict:
        """Place a simulated order against a sandbox SGI."""
        body = {"symbol": symbol, "side": side, "qty": qty}
        if sgi_id is not None:
            body["sgi_id"] = sgi_id
        return self._request("POST", "/orders", json=body)

    def order_get(self, order_id: str) -> dict:
        """Fetch a previously-created order by id."""
        return self._request("GET", f"/orders/{order_id}")

    def kyc_fetch(self, user_id: str) -> dict:
        """Fetch a mock Ed25519-signed KYC attestation for a user id."""
        return self._request("GET", f"/kyc/{user_id}")

    def sandbox_reset(self) -> dict:
        """Reset the demo wallet."""
        return self._request("POST", "/sandbox/reset")

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self._session.close()

    def __enter__(self) -> "InopayClient":
        return self

    def __exit__(self, *_exc: Any) -> None:
        self.close()
