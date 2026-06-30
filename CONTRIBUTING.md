# Contributing

Thank you for considering contributing to the Loga SMS Python SDK!

## Issues

- Use the [issue tracker](https://github.com/loga-engineering/loga-sms-sdk-python/issues) to report bugs or request features.
- Before opening a new issue, check if a similar one already exists.
- Provide a clear description, reproduction steps, and environment details for bugs.

## Pull Requests

1. Fork the repository and create a feature branch from `main`.
2. Write clear, concise commit messages following [Conventional Commits](https://www.conventionalcommits.org/).
3. Run tests locally with `pytest` before submitting.
4. Ensure your code follows [PEP 8](https://peps.python.org/pep-0008/) style guidelines.
5. Include a **Developer Certificate of Origin (DCO)** sign-off in each commit message:
   ```
   Signed-off-by: Your Name <your.email@example.com>
   ```
   By signing off you certify that you have the right to submit the contribution under the MIT license.

## Development Setup

```bash
git clone https://github.com/loga-engineering/loga-sms-sdk-python.git
cd loga-sms-sdk-python
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest
```

## Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/).
- Use type hints for all public API functions.
- Keep public API surface minimal and well-documented.
