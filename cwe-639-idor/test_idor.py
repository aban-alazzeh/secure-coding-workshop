"""
CWE-639 - Insecure Direct Object Reference (IDOR) tests

These tests define SECURE behavior.
They verify that users can only access their own notes.
"""

from fastapi.testclient import TestClient
from app import app


def login(client, username, password):
    return client.post(
        "/login",
        data={"username": username, "password": password},
        follow_redirects=True,
    )


def test_user_can_view_own_note():
    client = TestClient(app)
    
    login(client, "alice", "alice123")
    
    r = client.get("/note", params={"id": 1})
    
    assert r.status_code == 200
    assert "Alice Shopping List" in r.text
    assert "Eggs, milk, bread" in r.text


def test_user_blocked_from_other_users_note():
    client = TestClient(app)
    
    login(client, "alice", "alice123")
    
    r = client.get("/note", params={"id": 3})
    
    assert r.status_code == 200
    
    assert "Bob Personal Journal" not in r.text
    assert "great day" not in r.text
    
    assert "not authorized" in r.text.lower() or "access denied" in r.text.lower()


def test_user_can_create_note():
    client = TestClient(app)
    
    login(client, "alice", "alice123")
    
    r = client.post(
        "/create",
        data={"title": "Test Note", "content": "Test content"},
        follow_redirects=True,
    )
    
    assert r.status_code == 200
    assert "Test Note" in r.text


def test_unauthenticated_access_redirects():
    client = TestClient(app)
    
    r = client.get("/note", params={"id": 1}, follow_redirects=False)
    
    assert r.status_code in (302, 307)


def test_note_listing_shows_only_own_notes():
    client = TestClient(app)
    
    login(client, "alice", "alice123")
    
    r = client.get("/notes")
    
    assert r.status_code == 200
    
    assert "Alice Shopping List" in r.text
    assert "Alice Meeting Notes" in r.text
    
    assert "Bob Personal Journal" not in r.text
    assert "Charlie Ideas" not in r.text


def test_no_error_leakage_on_idor_attempt():
    client = TestClient(app, raise_server_exceptions=False)
    
    login(client, "charlie", "charlie123")
    
    r = client.get("/note", params={"id": 1})
    
    body = r.text.lower()
    
    assert "traceback" not in body
    assert "keyerror" not in body
    assert "exception" not in body
