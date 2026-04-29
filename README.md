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

## Why Inopay

Inopay is the [investment infrastructure for African capital markets](https://getinopay.com/fr/why-inopay) — BRVM (WAEMU), BVMAC (CEMAC), GSE (Ghana). Mobile Money operators, banks and licensed SGIs embed the regional exchanges into their apps via this SDK.

- Use case **Mobile Money operators** → see [Pour opérateurs MoMo](https://getinopay.com/fr/momo)
- Use case **Banks** → see [Pour banques](https://getinopay.com/fr/banks)
- Use case **SGI** → see [Pour SGI](https://getinopay.com/fr/sgi)
- White-label deployment → see [White-label](https://getinopay.com/fr/white-label)

## Regulatory framework

Inopay is a technical intermediation provider. Orders are executed exclusively by [AMF-UMOA-licensed SGIs](https://getinopay.com/fr/legal/regulatory-references). The KYC framework aligns with BCEAO Instruction No. 003-03-2025.

- [Compliance & doctrine (AMF-UMOA, COSUMAF, SEC Ghana)](https://getinopay.com/fr/compliance)
- [Public regulatory references](https://getinopay.com/fr/legal/regulatory-references)
- [Trust center & data residency](https://getinopay.com/fr/trust)
- [Contractual SLA](https://getinopay.com/fr/sla)
- [Public audit chain](https://getinopay.com/fr/audit)

## Other Inopay SDKs

The Inopay SDK family — same API surface, five native platforms:

- [`@inopay/web`](https://github.com/fofanay/inopay-web) — TypeScript / Web
- [`InopaySDK`](https://github.com/fofanay/inopay-ios) — Swift / iOS / macOS
- [`inopay-android`](https://github.com/fofanay/inopay-android) — Kotlin / Android / JVM
- [`inopay`](https://github.com/fofanay/inopay-python) — Python (sync, requests-based)
- [`inopay-java`](https://github.com/fofanay/inopay-java) — Java (sync, java.net.http + Jackson)

## Documentation & support

- [Developer portal](https://getinopay.com/fr/developers) — API, webhooks, sandbox
- [API reference (OpenAPI 3.1)](https://api.getinopay.com/v1/openapi.json)
- [Sandbox console](https://getinopay.com/fr/developers/sandbox) — public demo key + 7 endpoints
- [Portable KYC spec](https://getinopay.com/fr/developers/kyc) — Ed25519, offline-verifiable
- [Webhooks reference](https://getinopay.com/fr/developers/webhooks)
- [Changelog](https://getinopay.com/fr/developers/changelog)
- [Press kit](https://getinopay.com/fr/press-kit) — logo, boilerplates, fact sheet

Need integration help? Email <partner@getinopay.com>.

## License

MIT — © Inopay
