"""
Test suite for HTML sanitizer
"""

import pytest
from sanitizer import sanitize_html


def test_script_tags_blocked():
    """Script tags should be completely removed"""
    result = sanitize_html("<script>alert('xss')</script>")
    assert "<script>" not in result.lower()
    assert "alert" not in result


def test_img_tags_blocked():
    """Image tags should be removed"""
    result = sanitize_html('<img src=x onerror=alert(1)>')
    assert "<img" not in result.lower()


def test_bold_tags_allowed():
    """Bold tags should be preserved"""
    result = sanitize_html("<b>bold text</b>")
    assert "<b>bold text</b>" == result


def test_italic_tags_allowed():
    """Italic tags should be preserved"""
    result = sanitize_html("<i>italic text</i>")
    assert "<i>italic text</i>" == result


def test_underline_tags_allowed():
    """Underline tags should be preserved"""
    result = sanitize_html("<u>underlined text</u>")
    assert "<u>underlined text</u>" == result


def test_attributes_stripped():
    """All attributes should be removed, even from safe tags"""
    result = sanitize_html('<b onclick="alert(1)">text</b>')
    assert "onclick" not in result.lower()
    assert "<b>text</b>" == result


def test_mixed_content():
    """Safe and dangerous tags mixed together"""
    result = sanitize_html('<b>Safe</b><script>alert(1)</script><i>Also safe</i>')
    assert "<b>Safe</b>" in result
    assert "<i>Also safe</i>" in result
    assert "alert" not in result


def test_nested_tags():
    """Nested safe tags should work"""
    result = sanitize_html("<b>Bold <i>and italic</i></b>")
    assert "<b>Bold <i>and italic</i></b>" == result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
