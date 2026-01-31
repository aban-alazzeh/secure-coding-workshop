# CWE-79: Cross-Site Scripting (XSS)

This lab demonstrates how XSS happens when user input is rendered into an HTML page without proper output encoding.

You will run a small web app with a comment form. In the vulnerable version, the app renders user input as raw HTML. Your task is to fix the code so user input is displayed safely as text and cannot be interpreted as HTML/JavaScript.

Rules:
- You may modify `templates/comment.html` and/or `app.py` to fix the issue.
- Do NOT change tests.
- Do NOT add new dependencies.

Setup (run commands from inside `cwe-79-xss`):

Linux/macOS:
python3 -m venv .venv
source .venv/bin/activate

Windows PowerShell:
python -m venv .venv
.\.venv\Scripts\Activate.ps1

Install dependencies:
python -m pip install -r requirements.txt

Run tests (expected to FAIL at first):
python -m pytest -q

Run the app:
python -m uvicorn app:app --reload

Open in your browser:
http://127.0.0.1:8000/comment

What to try (for understanding only):
Submit a comment containing HTML tags. In the vulnerable version, tags may be rendered as real HTML.

Success criteria:
- Tests pass
- User input is displayed as text (escaped), not executed/rendered as raw HTML
