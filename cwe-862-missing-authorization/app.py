from pathlib import Path

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI(title="CWE-862 Missing Authorization Lab")

app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-key-change-this",
)

BASE_DIR = Path(__file__).resolve().parent
REPORTS_DIR = BASE_DIR / "data" / "reports"

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

USERS = {
    "alice": {"password": "alice123", "role": "user"},
    "bob": {"password": "bob123", "role": "admin"},
}

REPORT_ACCESS = {
    "public-report.txt": "user",
    "admin-report.txt": "admin",
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

    return RedirectResponse("/reports", status_code=302)


@app.get("/reports", response_class=HTMLResponse)
def list_reports(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/", status_code=302)

    report_names = sorted(
        p.name for p in REPORTS_DIR.iterdir() if p.is_file()
    )

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "user": user, "report_names": report_names},
    )


@app.get("/report", response_class=HTMLResponse)
def view_report(request: Request, name: str = ""):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/", status_code=302)

    error = None
    content = ""

    if not name:
        error = "Please select a report."
    else:
        target = REPORTS_DIR / name

        if not target.exists():
            error = "Report not found."
        else:
            # ❌ VULNERABILITY: Authorization NOT enforced
            content = target.read_text(encoding="utf-8")

    return templates.TemplateResponse(
        "report.html",
        {
            "request": request,
            "user": user,
            "name": name,
            "content": content,
            "error": error,
        },
    )
