"""
HTML Sanitizer - XSS Prevention Lab

Your task: Implement a sanitizer that prevents XSS attacks using an allowlist approach.

Requirements:
- Allow only these tags: <b>, <i>, <u>
- Block all other tags
- Strip ALL attributes from all tags
"""

from html.parser import HTMLParser


# TODO: Define your allowlist of safe tags here
ALLOWED_TAGS = None  # Replace None with your allowlist


class SafeHTMLParser(HTMLParser):
    """
    Custom HTML parser that sanitizes user input.
    
    You need to implement all the methods below.
    """
    
    def __init__(self):
        super().__init__()
        # TODO: Initialize any variables you need
        pass
        
    def handle_starttag(self, tag, attrs):
        """
        Called when the parser finds an opening tag like <b> or <script>
        
        Args:
            tag (str): The tag name (e.g., 'b', 'script', 'img')
            attrs (list): List of (attribute, value) tuples
        
        TODO: Implement this method
        """
        pass
        
    def handle_endtag(self, tag):
        """
        Called when the parser finds a closing tag like </b> or </script>
        
        Args:
            tag (str): The tag name
        
        TODO: Implement this method
        """
        pass
        
    def handle_data(self, data):
        """
        Called when the parser finds text content between tags
        
        Args:
            data (str): The text content
        
        TODO: Implement this method
        """
        pass
        
    def get_sanitized_html(self):
        """
        Returns the sanitized HTML as a string.
        
        TODO: Implement this method
        """
        pass


def sanitize_html(user_input: str) -> str:
    """
    INTENTIONALLY INSECURE (starter state)

    This returns raw user input so stored XSS is possible.
    Learners will later replace this with a real sanitizer.
    """
    return user_input or ""
