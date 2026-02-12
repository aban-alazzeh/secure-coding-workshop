# CWE-639: Insecure Direct Object Reference (IDOR) Lab

## Objective

Understand how failing to validate object ownership can allow authenticated users to access resources belonging to other users, and learn how to implement proper ownership-based access control.

## The Problem

The application allows users to create and view personal notes. Each note has a unique ID and belongs to a specific user.

Users authenticate with their credentials and can browse their own notes. However, when viewing a specific note by its ID, the application does not verify that the note belongs to the currently logged-in user.

As a result:
- Any authenticated user can view any note by guessing or iterating through note IDs.
- Personal information is exposed to other users.
- Horizontal privilege escalation is possible (user-to-user access).

## Your Task

Inspect the code and fix the missing ownership checks so that:

1. Authenticated users can only access their own notes.
2. Attempts to access other users' notes are blocked with an appropriate error message.
3. Unauthorized access attempts do not leak sensitive information.
4. The note listing page only shows the current user's notes.

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
* **Login as alice:**
   * `Username: alice`
   * `Password: alice123`
   * View your notes (IDs 1, 2)
   * Try accessing `/note?id=3` (Bob's note - should fail after fix)
* **Login as bob:**
   * `Username: bob`
   * `Password: bob123`
   * View your notes (IDs 3, 4)
* **Login as charlie:**
   * `Username: charlie`
   * `Password: charlie123`
   * View your notes (IDs 5, 6)

## Hints

<details>
<summary>Hint 1: Object Ownership</summary>

  Every object (note) has an owner. Before allowing access, verify that the currently authenticated user IS the owner of the requested object.
</details>

<details>
<summary>Hint 2: Check Before Serving</summary>

  Before displaying note content, compare the note's owner field with the current user's username. If they don't match, deny access.
</details>

<details>
<summary>Hint 3: Direct Object References</summary>

  Sequential IDs (1, 2, 3...) are predictable. Even if you hide IDs from the UI, attackers can guess them. The real protection is server-side ownership validation.
</details>
