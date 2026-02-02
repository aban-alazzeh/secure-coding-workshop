from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from db import authenticate_user, init_db

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "message": None},
    )


@app.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    # ❌ Intentionally weak:
    # - Relies on vulnerable DB code
    # - No error handling for DB failures
    ok = authenticate_user(username, password)

    if ok:
        message = f"✅ Welcome, {username}!"
    else:
        message = "❌ Invalid credentials."

    return templates.TemplateResponse(
        "login.html",
        {"request": request, "message": message},
    )
