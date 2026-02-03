# CWE-89: SQL Injection Lab

## Objective

Understand how unsafe construction of SQL queries can lead to different types of SQL injection vulnerabilities, and learn how to fix them using secure coding practices.

## The Problem

The application builds SQL queries by directly concatenating user-controlled input into SQL statements.

As a result:
- Authentication logic can be bypassed.
- Database error messages are leaked to users.
- Sensitive data can be extracted from the database.

## Your Task

Inspect the code and fix the insecure SQL usage so that::

1. Authentication cannot be bypassed using SQL injection.
2. Database error messages are not reflected back to the user.
3. SQL injection cannot be used to extract sensitive data.

Do **not** remove functionality or disable endpoints.  
Fix the vulnerabilities at their source.

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Test Your Solution
```bash
python -m pytest -q
```

**Goal:** All 6 tests should pass.

## Run the App
```bash
uvicorn app:app --reload
```

Visit: `http://127.0.0.1:8000`

**Try these:**
- Authentication bypass on the POST /login endpoint:
  - Username: admin' -- / admin 'OR '1'='1
  - Password: anything
- Error-based SQL Injection on the POST /debug endpoint:
  - ```bash
    '
    ```
- UNION-based SQL Injection on the GET /users endpoint:
  - ```bash
    ' UNION SELECT password FROM users --
    ```

## Hints

<details>
<summary>Hint 1: Parameterized Queries</summary>

  Avoid building SQL queries using string concatenation or f-strings.
</details>

<details>
<summary>Hint 2: Error Handling</summary>

  Database errors should never be shown to end users.
  Catch database exceptions and return a **generic error message** instead of the raw exception details.
</details>

<details>
<summary>Hint 3: Fix the Root Cause</summary>

  Blocking specific inputs or payloads is not sufficient.
  The correct fix ensures that user input is never interpreted as SQL, regardless of its contents.
</details>
