from fastapi.testclient import TestClient
from app import app


def login(client, username, password):
    return client.post(
        "/login",
        data={"username": username, "password": password},
        follow_redirects=True,
    )


def test_admin_can_access_admin_panel():
    client = TestClient(app)

    login(client, "admin", "admin123")

    r = client.get("/admin")

    assert r.status_code == 200
    assert "System Settings" in r.text


def test_regular_user_cannot_access_admin_panel():
    client = TestClient(app)

    login(client, "alice", "alice123")

    r = client.get("/admin")

    assert r.status_code == 200
    assert "access denied" in r.text.lower() or "not authorized" in r.text.lower()


def test_regular_user_cannot_modify_settings():
    client = TestClient(app)

    login(client, "bob", "bob123")

    r = client.post(
        "/admin/update",
        data={
            "maintenance_mode": "true",
            "site_banner": "Hacked Banner",
        },
        follow_redirects=True,
    )

    assert "Hacked Banner" not in r.text


def test_unauthenticated_user_redirected():
    client = TestClient(app)

    r = client.get("/admin", follow_redirects=False)

    assert r.status_code in (302, 307)
