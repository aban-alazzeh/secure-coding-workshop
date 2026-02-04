"""
CWE-22 — Path Traversal tests

These tests define what SECURE behavior looks like.
They will FAIL on the intentionally vulnerable implementation.
After fixing the code properly, all tests should PASS.
"""

from fastapi.testclient import TestClient
from app import app


def test_legit_report_can_be_viewed():
    client = TestClient(app)
    r = client.get("/report", params={"name": "welcome.txt"})
    assert r.status_code == 200
    assert "Welcome to the bank portal" in r.text


def test_missing_report_is_graceful():
    client = TestClient(app)
    r = client.get("/report", params={"name": "does-not-exist.txt"})
    assert r.status_code == 200
    assert "Report not found." in r.text


# -------------------------
# Traversal payloads
# -------------------------
def test_simple_dotdot_traversal_must_fail():
    client = TestClient(app)
    r = client.get("/report", params={"name": "../secret.txt"})
    assert r.status_code == 200

    # Must not leak the secret file content
    assert "internal-key=" not in r.text

    # Should be handled as not found / invalid
    assert "Report not found." in r.text or "Please provide a report name." in r.text


def test_nested_dotdot_traversal_must_fail():
    client = TestClient(app)
    r = client.get("/report", params={"name": "../../app.py"})
    assert r.status_code == 200

    # Must not leak application source
    assert "FastAPI" not in r.text
    assert "CWE-22 Path Traversal Lab" not in r.text

    assert "Report not found." in r.text or "Please provide a report name." in r.text


def test_url_encoded_traversal_must_fail():
    client = TestClient(app)

    # %2e%2e%2f == ../
    r = client.get("/report?name=%2e%2e%2fsecret.txt")
    assert r.status_code == 200
    assert "internal-key=" not in r.text
    assert "Report not found." in r.text or "Please provide a report name." in r.text


def test_absolute_path_must_fail():
    client = TestClient(app)

    # Not portable across OS, but the secure fix should block absolute paths anyway.
    r = client.get("/report", params={"name": "/etc/passwd"})
    assert r.status_code == 200

    # If the app is running on Linux, /etc/passwd has "root:" in it. Must not leak it.
    assert "root:" not in r.text
    assert "Report not found." in r.text or "Please provide a report name." in r.text


# -------------------------
# No internal leakage
# -------------------------
def test_must_not_leak_tracebacks_or_paths_on_errors():
    client = TestClient(app, raise_server_exceptions=False)

    # Force weird input that might trigger exceptions in bad fixes
    r = client.get("/report", params={"name": "\x00"})
    assert r.status_code in (200, 400)

    body = r.text.lower()
    assert "traceback" not in body
    assert "filenotfounderror" not in body
    assert "valueerror" not in body
    assert "permissionerror" not in body

    # avoid leaking absolute project paths
    assert "/mnt/" not in body
    assert "/home/" not in body
