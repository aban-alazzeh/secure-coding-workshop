# CWE-284: Improper Access Control Lab

## Objective

Understand how failing to enforce role-based authorization checks can allow authenticated users to access administrative functions they should not be permitted to use, and learn how to implement proper server-side role-based access control (RBAC).

## The Problem

The application requires users to log in before accessing protected resources. Each user is assigned a role (e.g., `user` or `admin`).

An authorization policy should restrict administrative functions to users with the `admin` role. However, the application does not properly enforce this policy when accessing the admin panel and system settings.

As a result:
- Regular users can access the admin panel.
- Regular users can modify system-wide settings.
- Sensitive configuration data is exposed to unauthorized users.
- Role-based access control is effectively bypassed.

## Your Task

Inspect the code and fix the missing authorization checks so that:

1. Authenticated users can access features appropriate for their role.
2. Admin-only endpoints (admin panel and settings updates) are blocked for normal users.
3. Unauthorized access attempts return a safe, informative error message.
4. Sensitive system settings are never exposed to users without admin privileges.

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

**Goal:** All 4 tests should pass.

## Run the App
```bash
uvicorn app:app --reload
```

Visit: `http://127.0.0.1:8000`

**Try these:**
* **Login as a regular user:**
   * `Username: alice`
   * `Password: alice123`
   * `Navigate to /notes (Should work - this demonstrates proper access control)`
   * `Navigate to /admin (Should fail after the fix is implemented)`
* **Login as an admin:**
   * `Username: admin`
   * `Password: admin123`
   * `Navigate to /admin (Should work)`
   * `Modify system settings (Should work)`
* **Attempt to modify settings as a regular user:**
   * Login as `bob` / `bob123`
   * `Try to POST to /admin/update (Should fail after the fix is implemented)`

## Hints

<details>
<summary>Hint 1: Authentication vs Authorization</summary>

  Authentication verifies the identity of a user.
  Authorization determines what that user is allowed to access.
  Both must be enforced on the server side.
</details>

<details>
<summary>Hint 2: Enforce Role Checks Before Access</summary>

  Before returning sensitive data or allowing state changes, verify that the logged-in user's role matches the required role. A helper function to check for admin privileges can centralize this logic.
</details>

<details>
<summary>Hint 3: Fix the Root Cause</summary>

  The correct fix ensures that administrative resources are never accessed unless authorization checks pass. Authorization must occur before settings are exposed and before any modifications are allowed.
</details>
