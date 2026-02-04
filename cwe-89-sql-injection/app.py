from fastapi import FastAPI, Form, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from db import authenticate_user, debug_lookup, init_db, search_users

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
def startup() -> None:
    init_db()


# -------------------------
# UI: Login page
# -------------------------
@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "message": None, "debug_error": None},
    )


# -------------------------
# 1) Boolean-based SQLi (auth bypass)
# -------------------------
@app.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    result = authenticate_user(username, password)

    if result:
        message = f"✅ Welcome, {result}!"
    else:
        message = "❌ Invalid credentials."

    return templates.TemplateResponse(
        "login.html",
        {"request": request, "message": message, "debug_error": None},
    )


# -------------------------
# 2) Error-based SQLi (leak SQL errors back to user)
# -------------------------
@app.post("/debug", response_class=HTMLResponse)
def debug_endpoint(request: Request, q: str = Form(...)):
    """
    INTENTIONALLY INSECURE:
    - Runs an unsafe query
    - Reflects raw DB error back to the user (error leakage)
    """
    try:
        rows = debug_lookup(q)
        message = f"Debug query returned {len(rows)} row(s)."
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "message": message, "debug_error": None},
        )
    except Exception as e:
        # ❌ Intentional error leakage for demo
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "message": None, "debug_error": str(e)},
        )


# -------------------------
# 3) UNION-based SQLi (data exfil via search)
# -------------------------
@app.get("/users", response_class=HTMLResponse)
def users_page(request: Request, search: str = Query(default="")):
    rows = search_users(search)
    return templates.TemplateResponse(
        "users.html",
        {"request": request, "rows": rows, "search": search},
    )
