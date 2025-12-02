# Tests — Getting started

1. Add test/dev dependencies (examples):
   - pytest
   - pytest-asyncio (if you want async tests)
   - httpx
   - pytest-cov

   Example:
   pip install pytest httpx pytest-asyncio pytest-cov

2. Put the test helpers and tests under `tests/` and run:
   pytest -q

3. The provided `conftest.py` swaps the repo DB engine for an in-memory SQLite engine for the test session, creates all tables, and yields a TestClient for the app. Adjust if your db module exposes different names.

4. The example tests are templates: update endpoint paths, JSON payloads, and assertions to match your actual router behavior.