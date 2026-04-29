"""Inopay Python SDK — client for African capital markets infrastructure."""
from .client import (
    InopayClient,
    InopayError,
    Instrument,
    SGI,
    Order,
    KycAttestation,
)

__version__ = "0.1.0a2"
__all__ = [
    "InopayClient",
    "InopayError",
    "Instrument",
    "SGI",
    "Order",
    "KycAttestation",
]
