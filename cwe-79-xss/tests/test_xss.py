from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_xss_payload_is_not_rendered_as_html():
    payload = "<script>alert('xss')</script>"
    response = client.post("/comment", data={"comment": payload})
    body = response.text

    # The response must not contain a raw script tag
    assert "<script>" not in body
    assert "</script>" not in body

    # Instead, it should contain escaped output
    assert "&lt;script&gt;" in body
    assert "&lt;/script&gt;" in body
