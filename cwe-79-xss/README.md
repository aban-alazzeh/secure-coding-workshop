# CWE-79: Cross-Site Scripting (XSS) Lab

## Objective

Build an HTML sanitizer that prevents XSS attacks while allowing basic text formatting.

## The Problem

The comment system allows users to format text with `<b>`, `<i>`, and `<u>` tags. However, attackers can inject malicious code like `<script>alert('XSS')</script>`.

Your job: implement a sanitizer that blocks dangerous HTML while preserving safe formatting.

## Your Task

Complete the `sanitizer.py` file:

1. Define `ALLOWED_TAGS` - which tags are safe?
2. Implement `SafeHTMLParser` class methods
3. Implement `sanitize_html()` function

**Approach:** Use an **allowlist** - only permit specific safe tags, block everything else.

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Test Your Solution
```bash
pytest test_xss.py -v
```

**Goal:** All 8 tests should pass.

## Run the App
```bash
uvicorn app:app --reload
```

Visit: `http://127.0.0.1:8000/comment`

**Try these:**
- Safe: `This is <b>bold</b> and <i>italic</i>`
- Attack: `<script>alert('XSS')</script>`
- Attack: `<img src=x onerror=alert(1)>`
- Attack: `<b onclick="alert(1)">click me</b>`

## Hints

<details>
<summary>Hint 1: Allowlist</summary>

Define which tags are safe:
```python
ALLOWED_TAGS = {'b', 'i', 'u'}
```
</details>

<details>
<summary>Hint 2: Parser Structure</summary>

You need to:
- Build a list to accumulate safe HTML parts
- Track when you're inside dangerous tags (so you can skip their content)
- Rebuild HTML with only allowed tags (no attributes)
</details>

<details>
<summary>Hint 3: Using HTMLParser</summary>
```python
from html.parser import HTMLParser

parser = SafeHTMLParser()
parser.feed(user_input)
result = parser.get_sanitized_html()
```
</details>

## Success Criteria

- ✅ All tests pass
- ✅ Safe tags (`<b>`, `<i>`, `<u>`) are preserved
- ✅ Dangerous tags (`<script>`, `<img>`, etc.) are removed
- ✅ ALL attributes are stripped (including from safe tags)
- ✅ Text content is preserved

## After Completion

Your instructor will demonstrate an alternative approach using **output escaping** instead of allowlisting.
