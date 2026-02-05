# CWE-20: Improper Input Validation Lab

## Objective
Understand how lack of proper input validation can allow malicious or malformed data to be processed by an application, and learn how to implement strict validation rules to prevent exploitation.

## The Problem
The application accepts user input without proper validation:
- Missing or empty values are silently replaced with defaults.
- Non-integer formats like scientific notation (`1e3`) and floats (`2.5`) are accepted.
- Negative, zero, and unreasonably large values are processed without rejection.
- Discount values outside acceptable ranges (negative, >100, floats) are accepted.

As a result:
- Users can manipulate pricing by providing unexpected input.
- The application processes invalid data instead of rejecting it.
- Business logic can be bypassed through crafted inputs.

## Your Task
Inspect the code and implement proper input validation so that:
1. Required fields (quantity) are validated and cannot be missing or empty.
2. Quantity accepts only integer digits (1-20 range).
3. Discount is optional but must be an integer in the range 0-50 if provided.
4. Scientific notation, floats, negative values, and out-of-range inputs are rejected.

Do **not** remove functionality or disable endpoints.  
Fix the vulnerabilities by implementing proper validation in `validator.py`.

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

**Goal:** All 7 tests should pass.

## Run the App
```bash
uvicorn app:app --reload
```

Visit: `http://127.0.0.1:8000`

**Try these exploits:**
- Missing quantity field (should be rejected)
- Scientific notation: `1e3` (should be rejected)
- Float values: `2.5` (should be rejected)
- Negative quantities: `-5` (should be rejected)
- Zero quantity: `0` (should be rejected)
- Huge quantities: `999999` (should be rejected)
- Invalid discounts: `-10`, `51`, `10.5` (should be rejected)

## Hints

<details>
<summary>Hint 1: Validate Before Parsing</summary>

Check the raw string format before attempting to convert to int/float.
Use string methods like `.isdigit()` to ensure only valid integer digits are present.
</details>

<details>
<summary>Hint 2: Range Validation</summary>

After confirming the format is valid, check that the parsed integer falls within acceptable business logic ranges.
Quantity: 1-20, Discount: 0-50.
</details>

<details>
<summary>Hint 3: Required vs Optional</summary>

Quantity is required - reject `None` or empty strings.
Discount is optional - treat `None` or empty strings as 0, but still validate if a value is provided.
</details>

<details>
<summary>Hint 4: Clear Error Messages</summary>

Return specific error messages that help developers understand what went wrong, such as:
- "Quantity is required"
- "Quantity must be a positive integer between 1 and 20"
- "Discount must be an integer between 0 and 50"
</details>
