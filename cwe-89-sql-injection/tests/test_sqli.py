"""
CWE-89 — SQL Injection tests

These tests define what SECURE behavior looks like.
They will FAIL on the intentionally vulnerable implementation.
After fixing the code properly, all tests should PASS.
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


# -------------------------
# Boolean-based SQLi
# -------------------------
def test_login_sqli_bypass_must_fail():
    client = TestClient(app)
    r = client.post("/login", data={"username": "admin' --", "password": "x"})
    assert r.status_code == 200
    assert "Invalid credentials" in r.text


def test_login_or_true_injection_must_fail():
    client = TestClient(app)
    r = client.post("/login", data={"username": "' OR '1'='1", "password": "x"})
    assert r.status_code == 200
    assert "Invalid credentials" in r.text


# -------------------------
# Error-based SQLi
# -------------------------
def test_debug_must_not_leak_sql_errors():
    client = TestClient(app, raise_server_exceptions=False)
    r = client.post("/debug", data={"q": "'"})

    assert r.status_code in (200, 400)

    body = r.text.lower()
    assert "sqlite" not in body
    assert "operationalerror" not in body
    assert "traceback" not in body
    assert "db error leaked" not in body


# -------------------------
# UNION-based SQLi
# -------------------------
def test_union_based_must_not_exfiltrate_passwords():
    client = TestClient(app)
    payload = "' UNION SELECT password FROM users --"
    r = client.get("/users", params={"search": payload})

    assert r.status_code == 200
    assert "admin123" not in r.text
    assert "alice123" not in r.text
    assert "bob123" not in r.text
