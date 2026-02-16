from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from pathlib import Path

app = FastAPI(title="CWE-284 Improper Access Control Lab")

app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-key-change-this",
)

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "alice": {"password": "alice123", "role": "user"},
    "bob": {"password": "bob123", "role": "user"},
}

SYSTEM_SETTINGS = {
    "maintenance_mode": False,
    "site_banner": "Welcome to SecureNotes",
}

# Simple in-memory notes storage
NOTES = {
    "admin": ["Remember to review security policies", "Team meeting at 3 PM"],
    "alice": ["Finish project documentation", "Buy groceries"],
    "bob": ["Call dentist for appointment", "Review code changes"],
}


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

    request.session["user"] = {
        "username": username,
        "role": user["role"],
    }

    return RedirectResponse("/dashboard", status_code=302)


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/", status_code=302)

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": user},
    )


# ✅ PROPERLY SECURED ENDPOINT (Authentication required only)
@app.get("/notes", response_class=HTMLResponse)
def notes_page(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/", status_code=302)

    username = user["username"]
    user_notes = NOTES.get(username, [])

    return templates.TemplateResponse(
        "notes.html",
        {"request": request, "user": user, "notes": user_notes},
    )


@app.post("/notes/add")
def add_note(
    request: Request,
    note: str = Form(...),
):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/", status_code=302)

    username = user["username"]
    if username not in NOTES:
        NOTES[username] = []
    
    NOTES[username].append(note)

    return RedirectResponse("/notes", status_code=302)


# 🚨 VULNERABLE ENDPOINT (No role check)
@app.get("/admin", response_class=HTMLResponse)
def admin_panel(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/", status_code=302)

    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "user": user,
            "settings": SYSTEM_SETTINGS,
            "error": None,
        },
    )


# 🚨 VULNERABLE ACTION (No authorization enforcement)
@app.post("/admin/update")
def update_settings(
    request: Request,
    maintenance_mode: bool = Form(False),
    site_banner: str = Form(...),
):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/", status_code=302)

    SYSTEM_SETTINGS["maintenance_mode"] = maintenance_mode
    SYSTEM_SETTINGS["site_banner"] = site_banner

    return RedirectResponse("/admin", status_code=302)
