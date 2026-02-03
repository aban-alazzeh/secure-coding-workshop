from __future__ import annotations

import secrets
from typing import Dict, Any, Optional

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import db
from csrf import generate_csrf_token, validate_csrf_token

app = FastAPI(title="CWE-352 CSRF Lab")
templates = Jinja2Templates(directory="templates")

# Simple in-memory sessions:
# session_id -> {"username": str, "csrf": str}
SESSIONS: Dict[str, Dict[str, Any]] = {}


def get_session(request: Request) -> Optional[Dict[str, Any]]:
    sid = request.cookies.get("session_id")
    if not sid:
        return None
    return SESSIONS.get(sid)


def require_login(request: Request) -> Dict[str, Any]:
    session = get_session(request)
    if not session:
        raise HTTPException(status_code=401, detail="Not logged in")
    return session


def require_csrf(session: Dict[str, Any], provided_token: Optional[str]) -> None:
    """
    CSRF guard for state-changing actions.

    NOTE: This currently calls an intentionally insecure validator in csrf.py.
    Students will implement proper token generation + validation.
    """
    expected = session.get("csrf", "")
    if not validate_csrf_token(expected, provided_token):
        raise HTTPException(status_code=403, detail="CSRF validation failed")


@app.on_event("startup")
def _startup() -> None:
    db.init_db()


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    session = get_session(request)
    if session:
        return RedirectResponse(url="/dashboard", status_code=302)
    return RedirectResponse(url="/login", status_code=302)


@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if not db.authenticate(username, password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials."})

    # Create session
    session_id = secrets.token_urlsafe(24)

    # CSRF token (starter uses csrf.generate_csrf_token which is currently insecure)
    csrf_token = generate_csrf_token()

    SESSIONS[session_id] = {"username": username, "csrf": csrf_token}

    resp = RedirectResponse(url="/dashboard", status_code=302)
    resp.set_cookie("session_id", session_id, httponly=True)
    return resp


@app.post("/logout")
def logout(request: Request):
    sid = request.cookies.get("session_id")
    if sid and sid in SESSIONS:
        del SESSIONS[sid]
    resp = RedirectResponse(url="/login", status_code=302)
    resp.delete_cookie("session_id")
    return resp


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    session = require_login(request)
    username = session["username"]

    context = {
        "request": request,
        "username": username,
        "balance": db.get_balance(username),
        "email": db.get_email(username),
        "payees": db.list_payees(username),
        "transfers": db.recent_transfers(username, limit=10),
        # CSRF token should be rendered into forms (starter template is missing it)
        "csrf_token": session.get("csrf", ""),
        "message": None,
        "error": None,
    }
    return templates.TemplateResponse("dashboard.html", context)


@app.post("/transfer", response_class=HTMLResponse)
def do_transfer(
    request: Request,
    recipient: str = Form(...),
    amount: int = Form(...),
    csrf_token: Optional[str] = Form(None),
):
    session = require_login(request)

    # CSRF guard (currently ineffective until students implement it)
    require_csrf(session, csrf_token)

    sender = session["username"]
    ok, msg = db.transfer(sender, recipient, amount)

    username = sender
    context = {
        "request": request,
        "username": username,
        "balance": db.get_balance(username),
        "email": db.get_email(username),
        "payees": db.list_payees(username),
        "transfers": db.recent_transfers(username, limit=10),
        "csrf_token": session.get("csrf", ""),
        "message": msg if ok else None,
        "error": None if ok else msg,
    }
    return templates.TemplateResponse("dashboard.html", context)


@app.post("/payees/add", response_class=HTMLResponse)
def add_payee(
    request: Request,
    payee: str = Form(...),
    csrf_token: Optional[str] = Form(None),
):
    session = require_login(request)
    require_csrf(session, csrf_token)

    owner = session["username"]
    db.add_payee(owner, payee)

    context = {
        "request": request,
        "username": owner,
        "balance": db.get_balance(owner),
        "email": db.get_email(owner),
        "payees": db.list_payees(owner),
        "transfers": db.recent_transfers(owner, limit=10),
        "csrf_token": session.get("csrf", ""),
        "message": f"Payee '{payee}' added.",
        "error": None,
    }
    return templates.TemplateResponse("dashboard.html", context)


@app.post("/profile/email", response_class=HTMLResponse)
def change_email(
    request: Request,
    email: str = Form(...),
    csrf_token: Optional[str] = Form(None),
):
    session = require_login(request)
    require_csrf(session, csrf_token)

    username = session["username"]
    db.set_email(username, email)

    context = {
        "request": request,
        "username": username,
        "balance": db.get_balance(username),
        "email": db.get_email(username),
        "payees": db.list_payees(username),
        "transfers": db.recent_transfers(username, limit=10),
        "csrf_token": session.get("csrf", ""),
        "message": "Email updated.",
        "error": None,
    }
    return templates.TemplateResponse("dashboard.html", context)
