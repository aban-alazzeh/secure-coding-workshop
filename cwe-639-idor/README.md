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

Run the tests to verify your fix:
```bash
python -m pytest -q
```

**Expected Results:**
- **Before fix (vulnerable):** 5 passed, 1 failed
- **After fix (secure):** 6 passed (all tests pass)

The failing test demonstrates the IDOR vulnerability - users can access notes belonging to other users by manipulating the note ID parameter.

## Run the App
```bash
uvicorn app:app --reload
```

Visit: `http://127.0.0.1:8000`

**Try these experiments:**

### Test the Vulnerability (Before Fix):
1. **Login as alice:**
   - Username: `alice`
   - Password: `alice123`
   - View your notes (you should see notes with IDs 1, 2)
   
2. **Exploit the IDOR:**
   - While logged in as alice, manually visit: `/note?id=3`
   - You can see Bob's note! This should NOT be allowed.
   - Try `/note?id=5` to see Charlie's note

3. **Verify other users:**
   - Login as bob (`bob`/`bob123`) - owns notes 3, 4
   - Login as charlie (`charlie`/`charlie123`) - owns notes 5, 6

### Test Your Fix (After Fix):
1. Login as alice and try to access `/note?id=3`
2. You should see: "You are not authorized to view this note."
3. Alice's own notes (1, 2) should still work normally

## Hints

<details>
<summary>Hint 1: Object Ownership</summary>

Every object (note) has an owner. Before allowing access, verify that the currently authenticated user IS the owner of the requested object.

Compare `note["owner"]` with `user["username"]`.
</details>

<details>
<summary>Hint 2: Check Before Serving</summary>

Before displaying note content, add a conditional check:
- If the note's owner matches the current user → allow access
- If the note's owner does NOT match → deny access with an error message

Don't forget to set `note = None` when denying access to prevent data leakage!
</details>

<details>
<summary>Hint 3: Direct Object References</summary>

Sequential IDs (1, 2, 3...) are predictable. Even if you hide IDs from the UI, attackers can guess them. 

The real protection is **server-side ownership validation** - always verify on the backend that the user owns the resource they're requesting.
</details>
