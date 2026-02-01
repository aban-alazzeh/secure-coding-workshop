"""
Test suite for HTML sanitizer

These tests verify that your sanitize_html() function:
1. Removes dangerous tags and attributes
2. Preserves safe tags
3. Handles edge cases correctly
"""

import pytest
from sanitizer import sanitize_html


class TestDangerousContent:
    """Tests that dangerous content is removed"""
    
    def test_script_tag_removed(self):
        """Script tags should be completely removed"""
        input_html = "<script>alert('xss')</script>"
        result = sanitize_html(input_html)
        
        # Script tag should not appear in output
        assert "<script>" not in result.lower()
        assert "alert" not in result  # The dangerous code should be gone too
        
    def test_img_tag_with_onerror_removed(self):
        """Image tags with event handlers should be removed"""
        input_html = '<img src=x onerror=alert("xss")>'
        result = sanitize_html(input_html)
        
        # No img tag should be present
        assert "<img" not in result.lower()
        # No event handler should be present
        assert "onerror" not in result.lower()
        assert "alert" not in result
        
    def test_iframe_tag_removed(self):
        """Iframe tags should be completely removed"""
        input_html = '<iframe src="evil.com"></iframe>'
        result = sanitize_html(input_html)
        
        assert "<iframe" not in result.lower()
        
    def test_object_tag_removed(self):
        """Object tags should be removed"""
        input_html = '<object data="evil.swf"></object>'
        result = sanitize_html(input_html)
        
        assert "<object" not in result.lower()
        
    def test_event_handler_on_safe_tag_removed(self):
        """Event handlers on otherwise safe tags should be stripped"""
        input_html = '<b onclick="alert(1)">Click me</b>'
        result = sanitize_html(input_html)
        
        # Tag should be present but without the event handler
        assert "<b>" in result
        assert "</b>" in result
        assert "Click me" in result
        # Event handler must be gone
        assert "onclick" not in result.lower()
        assert "alert" not in result


class TestSafeTags:
    """Tests that safe tags are preserved"""
    
    def test_bold_tag_preserved(self):
        """<b> tags should be preserved"""
        input_html = "This is <b>bold</b> text"
        result = sanitize_html(input_html)
        
        assert "<b>bold</b>" in result
        assert "This is" in result
        assert "text" in result
        
    def test_italic_tag_preserved(self):
        """<i> tags should be preserved"""
        input_html = "This is <i>italic</i> text"
        result = sanitize_html(input_html)
        
        assert "<i>italic</i>" in result
        
    def test_underline_tag_preserved(self):
        """<u> tags should be preserved"""
        input_html = "This is <u>underlined</u> text"
        result = sanitize_html(input_html)
        
        assert "<u>underlined</u>" in result
        
    def test_nested_safe_tags(self):
        """Nested safe tags should work correctly"""
        input_html = "<b>Bold with <i>nested italic</i> inside</b>"
        result = sanitize_html(input_html)
        
        assert "<b>" in result
        assert "<i>" in result
        assert "</i>" in result
        assert "</b>" in result
        assert "Bold with" in result
        assert "nested italic" in result
        
    def test_multiple_safe_tags(self):
        """Multiple different safe tags in sequence"""
        input_html = "<b>Bold</b> and <i>italic</i> and <u>underline</u>"
        result = sanitize_html(input_html)
        
        assert "<b>Bold</b>" in result
        assert "<i>italic</i>" in result
        assert "<u>underline</u>" in result


class TestAttributeStripping:
    """Tests that all attributes are stripped, even from safe tags"""
    
    def test_style_attribute_stripped(self):
        """Style attributes should be removed"""
        input_html = '<b style="color: red">Red text</b>'
        result = sanitize_html(input_html)
        
        # Tag should be present
        assert "<b>Red text</b>" in result
        # But style should be gone
        assert "style" not in result.lower()
        assert "color" not in result.lower()
        
    def test_class_attribute_stripped(self):
        """Class attributes should be removed"""
        input_html = '<b class="highlight">Text</b>'
        result = sanitize_html(input_html)
        
        assert "<b>Text</b>" in result
        assert "class" not in result.lower()
        assert "highlight" not in result.lower()
        
    def test_id_attribute_stripped(self):
        """ID attributes should be removed"""
        input_html = '<b id="myid">Text</b>'
        result = sanitize_html(input_html)
        
        assert "<b>Text</b>" in result
        assert "id=" not in result.lower()


class TestEdgeCases:
    """Tests for edge cases and complex scenarios"""
    
    def test_plain_text_unchanged(self):
        """Plain text without any HTML should pass through"""
        input_html = "Just plain text"
        result = sanitize_html(input_html)
        
        assert "Just plain text" in result
        
    def test_mixed_safe_and_dangerous(self):
        """Mix of safe and dangerous tags"""
        input_html = '<b>Safe</b><script>alert("xss")</script><i>Also safe</i>'
        result = sanitize_html(input_html)
        
        # Safe tags should be present
        assert "<b>Safe</b>" in result
        assert "<i>Also safe</i>" in result
        # Dangerous tag should be gone
        assert "<script>" not in result.lower()
        assert "alert" not in result
        
    def test_empty_input(self):
        """Empty string should return empty string"""
        result = sanitize_html("")
        assert result == ""
        
    def test_only_dangerous_tags(self):
        """Input with only dangerous tags"""
        input_html = '<script>evil()</script><iframe src="x"></iframe>'
        result = sanitize_html(input_html)
        
        # Should be mostly empty (maybe just the text content if you keep it)
        assert "<script>" not in result.lower()
        assert "<iframe>" not in result.lower()
        
    def test_javascript_protocol_in_href(self):
        """Even if we allowed <a>, javascript: protocol should be blocked"""
        # This test is optional since we don't allow <a> at all
        # But it shows awareness of URL-based XSS
        input_html = '<a href="javascript:alert(1)">Click</a>'
        result = sanitize_html(input_html)
        
        # Since <a> is not in ALLOWED_TAGS, it should be removed
        assert "javascript:" not in result.lower()
        
    def test_multiple_attributes_on_safe_tag(self):
        """Safe tag with multiple attributes - all should be stripped"""
        input_html = '<b class="x" id="y" onclick="z" style="color:red">Text</b>'
        result = sanitize_html(input_html)
        
        # Should only have the clean tag
        assert "<b>Text</b>" in result
        assert "class" not in result.lower()
        assert "id=" not in result.lower()
        assert "onclick" not in result.lower()
        assert "style" not in result.lower()


class TestIntegration:
    """Integration tests simulating real usage"""
    
    def test_realistic_comment_with_formatting(self):
        """A realistic user comment with formatting"""
        input_html = "I <b>really</b> like this <i>product</i>! It's <u>amazing</u>."
        result = sanitize_html(input_html)
        
        assert "I <b>really</b> like this <i>product</i>! It's <u>amazing</u>." == result
        
    def test_attempted_xss_in_formatted_comment(self):
        """User tries to inject XSS in a formatted comment"""
        input_html = 'This is <b>bold</b> and <script>alert("pwned")</script> not good'
        result = sanitize_html(input_html)
        
        # Formatting should work
        assert "<b>bold</b>" in result
        # XSS should be blocked
        assert "<script>" not in result.lower()
        assert "alert" not in result
        # Text should be preserved
        assert "This is" in result
        assert "not good" in result


if __name__ == "__main__":
    # Run tests with: python -m pytest test_xss_v2.py -v
    pytest.main([__file__, "-v"])
