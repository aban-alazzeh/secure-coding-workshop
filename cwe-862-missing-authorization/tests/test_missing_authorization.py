"""
CWE-862 — Missing Authorization tests

These tests define SECURE behavior.
They verify that authentication works and
authorization is properly enforced.
"""

from fastapi.testclient import TestClient
from app import app


# -------------------------------------------------
# Helper: login function
# -------------------------------------------------
def login(client, username, password):
    return client.post(
        "/login",
        data={"username": username, "password": password},
        follow_redirects=True,
    )


# -------------------------------------------------
# Public report should be accessible to normal user
# -------------------------------------------------
def test_public_report_accessible_to_user():
    client = TestClient(app)

    login(client, "alice", "alice123")

    r = client.get("/report", params={"name": "public-report.txt"})

    assert r.status_code == 200
    assert "Quarterly public performance overview" in r.text


# -------------------------------------------------
# Admin report accessible to admin
# -------------------------------------------------
def test_admin_report_accessible_to_admin():
    client = TestClient(app)

    login(client, "bob", "bob123")

    r = client.get("/report", params={"name": "admin-report.txt"})

    assert r.status_code == 200
    assert "Admin-only audit findings" in r.text


# -------------------------------------------------
# Admin report blocked for normal user
# -------------------------------------------------
def test_admin_report_blocked_for_normal_user():
    client = TestClient(app)

    login(client, "alice", "alice123")

    r = client.get("/report", params={"name": "admin-report.txt"})

    assert r.status_code == 200

    # Must not leak admin content
    assert "Admin-only audit findings" not in r.text

    # Must show authorization error
    assert "not authorized" in r.text.lower()


# -------------------------------------------------
# Missing authentication handled gracefully
# -------------------------------------------------
def test_missing_authentication_is_handled_gracefully():
    client = TestClient(app)

    r = client.get(
    "/report",
    params={"name": "public-report.txt"},
    follow_redirects=False,
    )

    assert r.status_code in (302, 307)



# -------------------------------------------------
# No internal leakage on auth failure
# -------------------------------------------------
def test_no_internal_leakage_on_authz_failure():
    client = TestClient(app, raise_server_exceptions=False)

    login(client, "alice", "alice123")

    r = client.get("/report", params={"name": "admin-report.txt"})

    body = r.text.lower()

    assert "traceback" not in body
    assert "keyerror" not in body
    assert "permissionerror" not in body
