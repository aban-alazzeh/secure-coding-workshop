"""
CWE-89 Lab: Tests that define what "secure" looks like.

Attendees must:
- Fix SQL injection using parameterized queries
- Prevent database error leakage
"""

from fastapi.testclient import TestClient
from app import app


def test_valid_login_works():
    client = TestClient(app)
    r = client.post("/login", data={"username": "alice", "password": "alice123"})
    assert r.status_code == 200
    assert "Welcome, alice" in r.text


def test_wrong_password_fails():
    client = TestClient(app)
    r = client.post("/login", data={"username": "alice", "password": "wrong"})
    assert r.status_code == 200
    assert "Invalid credentials" in r.text


def test_sqli_bypass_comment_injection_fails():
    client = TestClient(app)
    r = client.post(
        "/login",
        data={"username": "admin' --", "password": "doesnotmatter"},
    )
    assert r.status_code == 200
    assert "Invalid credentials" in r.text


def test_sqli_or_true_injection_fails():
    client = TestClient(app)
    r = client.post(
        "/login",
        data={"username": "' OR '1'='1", "password": "x"},
    )
    assert r.status_code == 200
    assert "Invalid credentials" in r.text


def test_unbalanced_quote_does_not_leak_sql_errors():
    client = TestClient(app, raise_server_exceptions=False)
    r = client.post(
        "/login",
        data={"username": "alice'", "password": "alice123"},
    )

    assert r.status_code in (200, 400)

    body = r.text.lower()
    assert "sqlite" not in body
    assert "operationalerror" not in body
    assert "traceback" not in body
