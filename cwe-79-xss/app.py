from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="CWE-79 Lab: Cross-Site Scripting (XSS)")

templates = Jinja2Templates(directory="templates")

@app.get("/comment", response_class=HTMLResponse)
def show_form(request: Request):
    return templates.TemplateResponse(
        "comment.html",
        {"request": request, "comment": None}
    )

@app.post("/comment", response_class=HTMLResponse)
def submit_comment(request: Request, comment: str = Form(...)):
    # INTENTIONALLY VULNERABLE: comment is rendered into HTML without proper escaping
    return templates.TemplateResponse(
        "comment.html",
        {"request": request, "comment": comment}
    )
