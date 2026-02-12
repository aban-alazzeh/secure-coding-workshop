# CWE-862: Missing Authorization Lab

## Objective

Understand how failing to enforce authorization checks can allow authenticated users to access resources they should not be permitted to view, and learn how to implement proper server-side role-based access control (RBAC).

## The Problem

The application requires users to log in before accessing report files. Each user is assigned a role (e.g., user or admin).

An authorization policy is defined that specifies which roles are allowed to access which reports. However, the application does not properly enforce this policy when serving report content.

As a result:
- Regular users can access admin-only reports.
- Sensitive information is exposed to unauthorized users.
- Role-based access control is effectively bypassed.

## Your Task

Inspect the code and fix the missing authorization checks so that:

1. Authenticated users can only access reports permitted for their role.
2. Admin-only reports are blocked for normal users.
3. Unauthorized access attempts return a safe, generic error message.
4. Sensitive report content is never leaked to users without sufficient privileges.

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
* **Login as a regular user:**
   * `Username: alice`
   * `Password: alice123`
   * `Attempt to access admin-report.txt (Should fail after the fix is implemented.)`
* **Login as an admin:**
   * `Username: bob`
   * `Password: bob123`
   * `access admin-report.txt`
* **Attempt direct access without login:**
   * `/report?name=public-report.txt`

## Hints

<details>
<summary>Hint 1: Authentication vs Authorization</summary>

  Authentication verifies the identity of a user.
  Authorization determines what that user is allowed to access.
  Both must be enforced on the server side.
</details>

<details>
<summary>Hint 2: Enforce the Policy Before Access</summary>

  Before reading or returning any file content, verify that the logged-in user's role matches the required role defined in the access policy.
</details>

<details>
<summary>Hint 3: Fix the Root Cause</summary>

  The correct fix ensures that sensitive resources are never accessed unless authorization checks pass. Authorization must occur before the file is read and before any content is returned.
</details>
