# CWE-352: Cross-Site Request Forgery (CSRF) Lab

## Objective

Understand how lack of CSRF protection allows attackers to perform unauthorized actions on behalf of authenticated users, and learn how to implement proper CSRF tokens to prevent these attacks.

## The Problem

The banking application performs state-changing operations (transfers, adding payees, updating email) without validating that requests actually came from the legitimate user interface.

As a result:
- Attackers can craft malicious pages that secretly submit requests to the bank.
- Victims' browsers automatically include session cookies with these forged requests.
- Money can be transferred, payees added, or account details changed without the user's knowledge.

## Your Task

Inspect the code and implement CSRF protection so that:

1. Each user session has a unique, unpredictable CSRF token.
2. All state-changing forms include this token.
3. The server validates the token before processing any state-changing request.

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

**Goal:** All tests should pass.

## Run the App
```bash
uvicorn app:app --reload
```

Visit: `http://127.0.0.1:8000`

**Try these attack scenarios:**

1. **Login as Alice:**
   - Username: `alice`
   - Password: `password123`

2. **Visit attacker pages (in the same browser while logged in):**
   - Transfer Attack: `http://127.0.0.1:8000/attacker/transfer`
   - Email Change Attack: `http://127.0.0.1:8000/attacker/change-email`
   - Add Payee Attack: `http://127.0.0.1:8000/attacker/add-payee`

3. **Observe:**
   - Before fix: Attacks succeed (money transferred, email changed, payee added)
   - After fix: Attacks fail with "CSRF validation failed" error

## Hints

<details>
<summary>Hint 1: Secure Token Generation</summary>

Use Python's `secrets` module to generate cryptographically random tokens:
```python
import secrets
token = secrets.token_urlsafe(32)
```
</details>

<details>
<summary>Hint 2: Token Storage</summary>

Store the CSRF token in the user's session when they log in.
Pass it to templates so forms can include it as a hidden field.
</details>

<details>
<summary>Hint 3: Token Validation</summary>

Before processing any POST request that changes state:
- Check that the token exists in the session
- Check that the token was provided in the form data
- Use constant-time comparison to prevent timing attacks
</details>

<details>
<summary>Hint 4: Where to Add Tokens</summary>

Add this line to every state-changing form in `dashboard.html`:
```html
<input type="hidden" name="csrf_token" value="{{ csrf_token }}" />
```
</details>

## Files to Modify

1. **`csrf.py`** - Implement `generate_csrf_token()` and `validate_csrf_token()`
2. **`dashboard.html`** - Add CSRF token hidden inputs to all three forms

