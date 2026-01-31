from fastapi.testclient import TestClient
from app import app, comments_db

client = TestClient(app)

def setup_function():
    """Clear comments before each test"""
    comments_db.clear()

def test_script_tag_is_sanitized():
    """Test that script tags are removed or escaped"""
    payload = "<script>alert('xss')</script>"
    response = client.post("/comment", data={"comment": payload})
    body = response.text

    # The response must not contain executable script tags
    assert "<script>" not in body.lower()
    assert "alert('xss')" not in body

def test_img_onerror_is_sanitized():
    """Test that event handlers in img tags are removed"""
    payload = '<img src=x onerror=alert("xss")>'
    response = client.post("/comment", data={"comment": payload})
    body = response.text

    # Event handlers should be stripped
    assert "onerror" not in body.lower()
    assert 'alert("xss")' not in body

def test_onmouseover_is_sanitized():
    """Test that inline event handlers are removed"""
    payload = '<div onmouseover="alert(1)">Hover me</div>'
    response = client.post("/comment", data={"comment": payload})
    body = response.text

    # Event handlers should be stripped
    assert "onmouseover" not in body.lower()
    assert "alert(1)" not in body

def test_javascript_protocol_is_sanitized():
    """Test that javascript: protocol in URLs is removed"""
    payload = '<a href="javascript:alert(1)">Click</a>'
    response = client.post("/comment", data={"comment": payload})
    body = response.text

    # javascript: protocol should be removed
    assert "javascript:" not in body.lower()

def test_safe_bold_tag_is_preserved():
    """Test that <b> tags are allowed and work correctly"""
    payload = "This is <b>bold text</b>"
    response = client.post("/comment", data={"comment": payload})
    body = response.text

    # <b> tags should be preserved
    assert "<b>bold text</b>" in body

def test_safe_italic_tag_is_preserved():
    """Test that <i> tags are allowed and work correctly"""
    payload = "This is <i>italic text</i>"
    response = client.post("/comment", data={"comment": payload})
    body = response.text

    # <i> tags should be preserved
    assert "<i>italic text</i>" in body

def test_safe_underline_tag_is_preserved():
    """Test that <u> tags are allowed and work correctly"""
    payload = "This is <u>underlined text</u>"
    response = client.post("/comment", data={"comment": payload})
    body = response.text

    # <u> tags should be preserved
    assert "<u>underlined text</u>" in body

def test_combined_safe_tags():
    """Test that multiple safe tags work together"""
    payload = "<b>Bold</b> and <i>italic</i> and <u>underline</u>"
    response = client.post("/comment", data={"comment": payload})
    body = response.text

    assert "<b>Bold</b>" in body
    assert "<i>italic</i>" in body
    assert "<u>underline</u>" in body

def test_stored_xss_persistence():
    """Test that stored comments persist and remain safe"""
    # Submit a malicious comment
    malicious = "<script>alert('stored xss')</script>"
    client.post("/comment", data={"comment": malicious})
    
    # Submit a safe comment
    safe = "This is <b>safe</b>"
    client.post("/comment", data={"comment": safe})
    
    # Get the page again (simulating a different user viewing stored comments)
    response = client.get("/comment")
    body = response.text
    
    # Malicious script should not be present
    assert "<script>" not in body.lower()
    assert "alert('stored xss')" not in body
    
    # Safe formatting should work
    assert "<b>safe</b>" in body

def test_multiple_vulnerabilities_in_one_comment():
    """Test that multiple XSS vectors in one comment are all sanitized"""
    payload = '<script>alert(1)</script><img src=x onerror=alert(2)><div onload=alert(3)>test</div>'
    response = client.post("/comment", data={"comment": payload})
    body = response.text
    
    # All malicious parts should be removed
    assert "<script>" not in body.lower()
    assert "onerror" not in body.lower()
    assert "onload" not in body.lower()
    assert "alert" not in body.lower()

def test_nested_safe_tags():
    """Test that nested safe tags work correctly"""
    payload = "<b>This is <i>nested</i> formatting</b>"
    response = client.post("/comment", data={"comment": payload})
    body = response.text
    
    # Nested tags should be preserved
    assert "<b>This is <i>nested</i> formatting</b>" in body

def test_unsafe_tag_with_safe_content():
    """Test that unsafe tags are removed even with safe-looking content"""
    payload = "<iframe>Safe text</iframe>"
    response = client.post("/comment", data={"comment": payload})
    body = response.text
    
    # iframe tags should be removed
    assert "<iframe>" not in body.lower()
    # But the text content should remain (depending on sanitization approach)
    # This test allows either stripping the tag or escaping it
