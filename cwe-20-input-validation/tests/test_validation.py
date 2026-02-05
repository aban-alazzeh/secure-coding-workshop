from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def _post_checkout(data: dict):
    return client.post("/api/checkout", data=data)


def test_missing_quantity_is_rejected():
    r = _post_checkout({"discount": "10"})
    assert r.status_code == 400
    assert r.json()["ok"] is False
    assert "quantity" in r.json()["error"].lower()


def test_quantity_must_be_integer_digits_only():
    r = _post_checkout({"quantity": "2.5", "discount": "0"})
    assert r.status_code == 400
    assert r.json()["ok"] is False


def test_quantity_scientific_notation_is_rejected():
    r = _post_checkout({"quantity": "1e3", "discount": "0"})
    assert r.status_code == 400
    assert r.json()["ok"] is False


def test_quantity_zero_or_negative_is_rejected():
    r1 = _post_checkout({"quantity": "0", "discount": "0"})
    r2 = _post_checkout({"quantity": "-2", "discount": "0"})
    assert r1.status_code == 400
    assert r2.status_code == 400


def test_quantity_too_large_is_rejected():
    r = _post_checkout({"quantity": "999999", "discount": "0"})
    assert r.status_code == 400
    assert r.json()["ok"] is False


def test_discount_must_be_integer_0_to_50():
    r1 = _post_checkout({"quantity": "2", "discount": "-1"})
    r2 = _post_checkout({"quantity": "2", "discount": "51"})
    r3 = _post_checkout({"quantity": "2", "discount": "10.5"})
    assert r1.status_code == 400
    assert r2.status_code == 400
    assert r3.status_code == 400


def test_valid_inputs_succeed_and_total_is_correct():
    r = _post_checkout({"quantity": "2", "discount": "10"})
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert body["quantity"] == 2
    assert body["discount"] == 10
    assert abs(body["total"] - 27.0) < 0.0001
