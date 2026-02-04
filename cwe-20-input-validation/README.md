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


**Try these attack payloads via the interactive docs:**

1. **Type confusion (should be rejected):**
```json
   {"q": 123}
```

2. **Excessive input length (should be rejected):**
```json
   {"q": "aaaaaaaaaa..."}  // 5000+ characters
```

3. **Invalid pagination (should be rejected):**
```json
   {"page": 0}
   {"page_size": 100000}
```

4. **Unintended sort field (should be rejected):**
```json
   {"sort": "-drop_table"}
   {"sort": "password_hash"}
```

5. **Empty or disallowed fields (should be rejected):**
```json
   {"fields": []}
   {"fields": ["password_hash", "secret_key"]}
```

6. **Invalid log levels (should be rejected):**
```json
   {"filters": {"level": ["INFO", "HACK"]}}
```

## Hints

<details>
<summary>Hint 1: Type Validation</summary>

Always check that inputs are the expected type before using them:
```python
if not isinstance(q, str):
    raise ValueError("'q' must be a string")
```
</details>

<details>
<summary>Hint 2: Range/Length Limits</summary>

Set reasonable boundaries for numeric and string inputs:
```python
if page < 1:
    raise ValueError("'page' must be >= 1")
if len(q) > 1000:
    raise ValueError("'q' must be <= 1000 characters")
```
</details>

<details>
<summary>Hint 3: Allowlisting</summary>

Use predefined sets to validate field names:
```python
ALLOWED_FIELDS = {"id", "service", "level", "timestamp", "message"}

for field in fields:
    if field not in ALLOWED_FIELDS:
        raise ValueError(f"Invalid field: {field}")
```
</details>

<details>
<summary>Hint 4: Sort Field Validation</summary>

Remember that sort can start with `-` for descending order:
```python
sort_field = sort.lstrip("-")
if sort_field not in ALLOWED_SORT_FIELDS:
    raise ValueError(f"Invalid sort field: {sort_field}")
```
</details>

## Files to Modify

**`validator.py`** - Add proper validation checks to `validate_and_normalize()`

## Validation Checklist

Your implementation should validate:

1. **`q` (search query):**
   - Must be a string
   - Maximum length: 1000 characters

2. **`page`:**
   - Must be an integer
   - Minimum value: 1

3. **`page_size`:**
   - Must be an integer
   - Maximum value: 100

4. **`sort`:**
   - Must be in `ALLOWED_SORT_FIELDS` (with or without `-` prefix)

5. **`fields`:**
   - Must be a non-empty list
   - All fields must be in `ALLOWED_FIELDS`

6. **`filters.level`:**
   - All levels must be in `ALLOWED_LEVELS`
