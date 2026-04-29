# inopay (Python SDK)

[![PyPI version](https://img.shields.io/pypi/v/inopay.svg)](https://pypi.org/project/inopay/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Inopay Python SDK — synchronous client for the African capital markets infrastructure (BRVM, BVMAC, GSE) via the public sandbox.

## Status

`v0.1.0a2` — public alpha. Wraps `https://api.getinopay.com/v1/sandbox/*`. PyPI publication coming next.

## Install

### From GitHub (during alpha)

```bash
pip install git+https://github.com/fofanay/inopay-python.git@v0.1.0-alpha.2
```

### From PyPI (coming soon)

```bash
pip install inopay
```

## Quick start

```python
from inopay import InopayClient

with InopayClient(api_key="sk_test_demo_inopay_2026") as inopay:
    # Health check
    print(inopay.health())  # {'sandbox': True, 'status': 'ok', ...}

    # List instruments
    result = inopay.instruments_list()
    for instrument in result["instruments"]:
        print(f"{instrument['symbol']}: {instrument['last_price']} {instrument['currency']}")

    # Place a simulated order
    order = inopay.order_create(symbol="SNTS.BRVM", side="buy", qty=10)
    print(f"Order {order['order']['id']} status: {order['order']['status']}")

    # Fetch a mock KYC attestation
    kyc = inopay.kyc_fetch("usr_demo_42")
    print(f"Attestation issued at {kyc['attestation']['issued_at']}")
```

## API surface

| Method | Description |
|---|---|
| `health()` | Sandbox status |
| `instruments_list()` | List BRVM / BVMAC / GSE instruments |
| `sgis_list()` | List partner SGIs |
| `order_create(symbol, side, qty, sgi_id=None)` | Place a simulated order |
| `order_get(order_id)` | Read back an order |
| `kyc_fetch(user_id)` | Mock Ed25519-signed KYC attestation |
| `sandbox_reset()` | Reset the demo wallet |

## Rate limit

The public demo key `sk_test_demo_inopay_2026` is rate-limited to **60 requests per minute per IP**.
For higher quotas request a private sandbox key at <https://getinopay.com/fr/developers/sandbox>.

## Requirements

- Python 3.9+
- `requests` 2.31+

## License

MIT — © Inopay
