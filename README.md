# Loga SMS Python SDK

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/loga-sms-sdk)](https://pypi.org/project/loga-sms-sdk/)
[![Python >=3.8](https://img.shields.io/pypi/pyversions/loga-sms-sdk)](https://pypi.org/project/loga-sms-sdk/)

**Official Python SDK for the Loga SMS Core Middleware API** — send and track SMS messages programmatically.

## Features

- SMS sending with `QUEUED`, `INSTANT`, `TRANSACTION`, `CAMPAIGN` priorities
- Delivery status checking by `external_ref_no` or `idempotency_key`
- OAuth2 client credentials authentication with automatic token refresh + 401 retry
- Idempotency-Key support (header-based, Stripe convention)
- Environment variable or constructor configuration
- Configurable HTTP timeout
- Type-annotated models (dataclasses)
- Python 3.8+ compatible

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Installation

```bash
pip install loga-sms-sdk
```

## Quick Start

```python
from loga_sms_sdk import LogaSmsClient

client = LogaSmsClient()
response = client.send('+22370000000', 'Hello from Python!')
print(f"Sent: {response.externalRefNo}")

# Check delivery status
status = client.check_status(response.externalRefNo)
print(f"Status: {status.status}")
```

## Configuration

The SDK can be configured via environment variables or constructor parameters:

| Environment Variable | Constructor Parameter | Required | Default |
|---|---|---|---|
| `LOGA_SMS_CLIENT_ID` | `client_id` | For OAuth | — |
| `LOGA_SMS_CLIENT_SECRET` | `client_secret` | For OAuth | — |
| `LOGA_SMS_API_KEY` | `api_key` | Yes | — |
| `LOGA_SMS_BASE_URL` | `base_url` | No | `https://api.sms.loga-apps.com` |
| `LOGA_SMS_DEFAULT_SENDER_NAME` | `default_sender_name` | No | — |
| `LOGA_SMS_DEFAULT_CALLBACK_URL` | `default_callback_url` | No | — |
| _(none)_ | `timeout` | No | `30` |

## Usage

### Creating a Client

```python
from loga_sms_sdk import LogaSmsClient

# All values from environment variables
client = LogaSmsClient()

# Or pass explicitly (overrides environment variables)
client = LogaSmsClient(
    client_id='your-client-id',
    client_secret='your-client-secret',
    api_key='your-api-key',
    base_url='https://api.sms.loga-apps.com',
    default_sender_name='MyApp',
    default_callback_url='https://myapp.com/sms-callback',
    timeout=15,
)
```

### Sending SMS

```python
from loga_sms_sdk import LogaSmsClient, SmsPriority

client = LogaSmsClient()

# Simple send (defaults to QUEUED priority)
response = client.send('+22370000000', 'Hello!')

# With all options
response = client.send(
    '+22370000000',
    'Urgent message',
    priority=SmsPriority.INSTANT,
    sender_name='MyApp',
    callback_url='https://myapp.com/sms-callback',
    idempotency_key='my-unique-key-789',
)
```

### Checking Status

```python
# By external reference number
status = client.check_status('ext-ref-123')
print(f"Status: {status.status}")
print(f"Receiver: {status.receiverAddress}")
print(f"Created: {status.createdAt}")

# By idempotency key
status = client.check_status(idempotency_key='my-idempotency-key-456')
print(f"Status: {status.status}")
```

### Error Handling

```python
from loga_sms_sdk import LogaSmsClient
from requests.exceptions import HTTPError

client = LogaSmsClient()

try:
    response = client.send('+22370000000', 'Hello!')
except HTTPError as e:
    print(f"HTTP {e.response.status_code}: {e}")
```

## API Reference

| Method | Parameters | Description |
|---|---|---|
| `send()` | `to, message, priority, sender_name, callback_url, idempotency_key` | Send an SMS with full control |
| `check_status()` | `external_ref_no, idempotency_key` | Check delivery status (provide at least one) |

### Response Models

| Class | Fields |
|---|---|
| `SMSSendResponse` | `externalRefNo`, `status`, `message` |
| `SmsStatusResponse` | `externalRefNo`, `status`, `receiverAddress`, `createdAt`, `updatedAt`, `message` |
| `SmsPriority` | Enum: `QUEUED`, `INSTANT`, `TRANSACTION`, `CAMPAIGN` |

## Examples

See the [examples/fastapi-app/](examples/fastapi-app/) directory for a complete FastAPI integration example.
