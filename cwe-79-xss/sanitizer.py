"""
HTML Sanitizer - XSS Prevention Lab

Your task: Implement the sanitize_html() function to prevent XSS attacks
while allowing safe HTML tags for formatting.

Requirements:
- Allow only these tags: <b>, <i>, <u>
- Remove all other tags completely
- Strip ALL attributes from all tags (including allowed ones)
- Preserve text content
- Handle nested tags correctly

You MUST use html.parser.HTMLParser for parsing.
You may NOT use external sanitization libraries.
"""

from html.parser import HTMLParser
import html


# Define which tags are safe to allow
ALLOWED_TAGS = {'b', 'i', 'u'}


class SafeHTMLParser(HTMLParser):
    """
    Custom HTML parser that builds safe HTML output.
    
    TODO: Implement the methods below to:
    1. Track opening and closing tags
    2. Only output allowed tags (without attributes)
    3. Escape text content properly
    4. Ignore/remove dangerous tags
    """
    
    def __init__(self):
        super().__init__()
        self.result = []  # List to build the safe HTML output
        # TODO: Add any other instance variables you need
        
    def handle_starttag(self, tag, attrs):
        """
        Called when parser encounters an opening tag like <b> or <script>
        
        Args:
            tag (str): The tag name (e.g., 'b', 'script', 'img')
            attrs (list): List of (attribute, value) tuples
        
        TODO: Implement this method
        - If tag is in ALLOWED_TAGS, append it to self.result (without attributes)
        - If tag is not allowed, ignore it (don't add to result)
        - Remember: we want to strip ALL attributes, even from safe tags
        
        Example:
            Input: <b onclick="alert('xss')">
            Output should add: <b>
            
            Input: <script>
            Output should add: nothing (ignore it)
        """
        # YOUR CODE HERE
        pass
        
    def handle_endtag(self, tag):
        """
        Called when parser encounters a closing tag like </b> or </script>
        
        Args:
            tag (str): The tag name
        
        TODO: Implement this method
        - If tag is in ALLOWED_TAGS, append closing tag to self.result
        - If tag is not allowed, ignore it
        
        Example:
            Input: </b>
            Output should add: </b>
            
            Input: </script>
            Output should add: nothing
        """
        # YOUR CODE HERE
        pass
        
    def handle_data(self, data):
        """
        Called when parser encounters text content between tags
        
        Args:
            data (str): The text content
        
        TODO: Implement this method
        - Always append the text data to self.result
        - Consider: should you escape the data? Why or why not?
        
        Example:
            Input: "Hello World"
            Output should add: "Hello World"
            
            Input: "<script>alert('xss')</script>" (as text, not tags)
            Output should add: escaped version to prevent execution
        """
        # YOUR CODE HERE
        pass
        
    def get_safe_html(self):
        """
        Returns the sanitized HTML as a string.
        
        TODO: Implement this method
        - Join all parts in self.result into a single string
        - Return the safe HTML
        """
        # YOUR CODE HERE
        return ""


def sanitize_html(dirty_html):
    """
    Sanitizes HTML input to prevent XSS attacks.
    
    This function should:
    1. Parse the input HTML
    2. Remove dangerous tags (script, iframe, img, etc.)
    3. Strip all attributes (including from safe tags)
    4. Keep only safe tags: b, i, u
    5. Preserve text content
    6. Return safe HTML that can be rendered
    
    Args:
        dirty_html (str): Potentially malicious HTML input
        
    Returns:
        str: Sanitized HTML safe to render
        
    Examples:
        >>> sanitize_html('<b>Hello</b>')
        '<b>Hello</b>'
        
        >>> sanitize_html('<script>alert("xss")</script>')
        'alert("xss")'  # or '' depending on your implementation
        
        >>> sanitize_html('<b onclick="alert()">Click</b>')
        '<b>Click</b>'
        
        >>> sanitize_html('This is <b>bold</b> and <i>italic</i>')
        'This is <b>bold</b> and <i>italic</i>'
    
    TODO: Implement this function
    Steps:
    1. Create an instance of SafeHTMLParser
    2. Feed it the dirty_html
    3. Get the sanitized result
    4. Return it
    """
    # YOUR CODE HERE
    # Hint: 
    # parser = SafeHTMLParser()
    # parser.feed(dirty_html)
    # return parser.get_safe_html()
    
    return dirty_html  # WRONG! This returns unsanitized input. Replace this.


# Optional: Add any helper functions you need below
