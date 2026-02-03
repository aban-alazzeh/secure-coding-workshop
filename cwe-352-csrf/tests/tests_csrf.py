import re
import pytest
from httpx import AsyncClient, ASGITransport

from app import app


@pytest.mark.anyio
async def test_login_sets_session_cookie():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post("/login", data={"username": "alice", "password": "password123"})
        assert r.status_code in (200, 302)
        # Cookie must exist
        assert "session_id" in client.cookies


@pytest.mark.anyio
async def test_dashboard_contains_csrf_token_field():
    """
    Secure version: dashboard forms must include a CSRF token hidden input.

    Starter version is intentionally missing it, so this test should FAIL
    until learners add the hidden field to the templates and implement token generation.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/login", data={"username": "alice", "password": "password123"})
        r = await client.get("/dashboard")
        assert r.status_code == 200

        html = r.text
        # Expect at least one csrf_token field rendered in HTML
        assert 'name="csrf_token"' in html, "Dashboard must render a csrf_token hidden field in forms."


@pytest.mark.anyio
async def test_transfer_requires_csrf_token():
    """
    Secure version: POST /transfer must reject requests without csrf_token.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/login", data={"username": "alice", "password": "password123"})

        r = await client.post("/transfer", data={"recipient": "attacker", "amount": "10"})
        assert r.status_code == 403, "Missing CSRF token must be rejected."


@pytest.mark.anyio
async def test_payee_add_requires_csrf_token():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/login", data={"username": "alice", "password": "password123"})

        r = await client.post("/payees/add", data={"payee": "attacker"})
        assert r.status_code == 403, "Missing CSRF token must be rejected."


@pytest.mark.anyio
async def test_email_change_requires_csrf_token():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/login", data={"username": "alice", "password": "password123"})

        r = await client.post("/profile/email", data={"email": "attacker@evil.test"})
        assert r.status_code == 403, "Missing CSRF token must be rejected."


@pytest.mark.anyio
async def test_valid_csrf_allows_transfer():
    """
    Secure version: if you fetch the CSRF token from the dashboard and send it back,
    the transfer should succeed (200).
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/login", data={"username": "alice", "password": "password123"})

        dash = await client.get("/dashboard")
        assert dash.status_code == 200

        # Extract token value from HTML input
        m = re.search(r'name="csrf_token"\s+value="([^"]+)"', dash.text)
        assert m, "csrf_token input must have a value attribute."
        token = m.group(1)
        assert token, "csrf_token value must not be empty."

        r = await client.post("/transfer", data={"recipient": "attacker", "amount": "10", "csrf_token": token})
        assert r.status_code == 200
        assert "Transfer complete" in r.text


@pytest.mark.anyio
async def test_wrong_csrf_is_rejected():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/login", data={"username": "alice", "password": "password123"})

        r = await client.post("/transfer", data={"recipient": "attacker", "amount": "10", "csrf_token": "WRONG"})
        assert r.status_code == 403
