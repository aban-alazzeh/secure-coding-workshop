from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from pathlib import Path

app = FastAPI(title="CWE-639 IDOR Lab")

app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-key-change-this",
)

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

USERS = {
    "alice": {"password": "alice123"},
    "bob": {"password": "bob123"},
    "charlie": {"password": "charlie123"},
}

# In-memory note storage with predictable sequential IDs
NOTES = {
    1: {"title": "Alice's Shopping List", "content": "Eggs, milk, bread, coffee", "owner": "alice"},
    2: {"title": "Alice's Meeting Notes", "content": "Discuss Q4 strategy with team", "owner": "alice"},
    3: {"title": "Bob's Personal Journal", "content": "Today was a great day. Learned about security vulnerabilities.", "owner": "bob"},
    4: {"title": "Bob's Password Hints", "content": "My dog's name + birth year", "owner": "bob"},
    5: {"title": "Charlie's Ideas", "content": "Build a note-taking app with better security", "owner": "charlie"},
    6: {"title": "Charlie's Private Thoughts", "content": "Need to change all my passwords after this lab", "owner": "charlie"},
}

# Counter for new note IDs
NEXT_NOTE_ID = 7


def get_current_user(request: Request):
    return request.session.get("user")


@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": None},
    )


@app.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    user = USERS.get(username)

    if not user or user["password"] != password:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid username or password."},
        )

    request.session["user"] = {"username": username}
    return RedirectResponse("/notes", status_code=302)


@app.get("/notes", response_class=HTMLResponse)
def list_notes(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/", status_code=302)

    # Filter notes to show only current user's notes
    user_notes = [
        {"id": note_id, **note}
        for note_id, note in NOTES.items()
        if note["owner"] == user["username"]
    ]

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "user": user, "notes": user_notes},
    )


@app.get("/note", response_class=HTMLResponse)
def view_note(request: Request, id: int = 0):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/", status_code=302)

    error = None
    note = None

    if id == 0:
        error = "Please select a note."
    else:
        note = NOTES.get(id)
        
        if not note:
            error = "Note not found."
        else:
            # ❌ VULNERABILITY: No ownership check!
            # Any authenticated user can view any note by ID
            pass  # Note will be displayed without verification

    return templates.TemplateResponse(
        "note.html",
        {
            "request": request,
            "user": user,
            "note": note,
            "note_id": id,
            "error": error,
        },
    )


@app.get("/create", response_class=HTMLResponse)
def create_note_page(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/", status_code=302)

    return templates.TemplateResponse(
        "create.html",
        {"request": request, "user": user},
    )


@app.post("/create")
def create_note(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
):
    global NEXT_NOTE_ID
    
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/", status_code=302)

    NOTES[NEXT_NOTE_ID] = {
        "title": title,
        "content": content,
        "owner": user["username"],
    }
    
    NEXT_NOTE_ID += 1
    
    return RedirectResponse("/notes", status_code=302)
