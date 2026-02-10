# CWE-22: Path Traversal Lab

## Objective

Understand how unsafe handling of user-controlled file paths can lead to path traversal vulnerabilities, and learn how to fix them using secure filesystem access patterns.

## The Problem

The application allows users to view report files by supplying a file name. The server constructs file paths by directly combining user input with a base directory.

As a result:
- Attackers can escape the intended directory using ../ path traversal.
- Sensitive files outside the reports folder can be accessed.
- Internal filesystem paths and application files may be exposed if errors are mishandled.

## Your Task

Inspect the code and fix the insecure file handling so that:

1. Legitimate report files inside the reports directory can still be viewed.
2. Path traversal attempts cannot escape the intended directory.
3. Absolute paths and encoded traversal payloads are blocked.
4. Internal errors, stack traces, and filesystem paths are not leaked to users.

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
* **Legitimate file access:**
   * `/report?name=welcome.txt`
* **Simple path traversal:**
   * `/report?name=../secret.txt`
* **Nested traversal:**
   * `/report?name=../../app.py`
* **URL-encoded traversal:**
   * `/report?name=%2e%2e%2fsecret.txt`

## Hints

<details>
<summary>Hint 1: Path Normalization</summary>

  User input should never be trusted as a filesystem path.
  Normalize and resolve paths before accessing the filesystem.
</details>

<details>
<summary>Hint 2: Enforce a Base Directory</summary>

  After resolving a path, verify that it still resides inside the intended base directory.
  If it escapes that directory, treat it as invalid.
</details>

<details>
<summary>Hint 3: Fix the Root Cause</summary>

  The correct fix ensures that user input can never cause the filesystem to access unintended locations, regardless of encoding or format.
</details>
