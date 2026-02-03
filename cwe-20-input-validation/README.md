# CWE-20: Improper Input Validation

## Objective

Understand how accepting unvalidated or weakly validated input can lead to security, reliability, and availability issues, even when no obvious crash or error occurs.

This lab focuses on defining what valid input actually is and enforcing those rules consistently.

## The Problem

The application provides a /search endpoint that lets users control how data is filtered and sorted.

In its current state, the application:
- Does not strictly check input types.
- Does not limit the size or range of values.
- Accepts user-supplied field names without restriction.

Because of this, the application:
- Accepts values that don’t make sense (for example, extremely large page sizes)
- Allows users to sort or request fields that were never intended to be exposed
- Continues processing requests that should have been rejected

## Your Task

Your task is to harden the input validation logic so that:

- Invalid input is rejected early
- Only expected types, values, and fields are accepted
- The application fails safely with a clear error

You must:
- Modify the input validation logic
- Clearly define what “valid input” means
- Reject everything else

You **must not**:
- Change the tests
- Change the application’s core logic


## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run the App
```bash
uvicorn app:app --reload
```

Visit: `http://127.0.0.1:8000/docs`

## Test Your Solution
```bash
python -m pytest -q
```

**Goal:** All 6 tests should pass.


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
