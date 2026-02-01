from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

app = FastAPI()
templates = Jinja2Templates(directory=".")

comments = []

@app.get("/comment", response_class=HTMLResponse)
def show_form(request: Request):
    return templates.TemplateResponse(
        "comment.html",
        {"request": request, "comments": comments},
    )

@app.post("/comment", response_class=HTMLResponse)
def submit_comment(request: Request, comment: str = Form(...)):
    # Store raw user input (untrusted)
    comments.append(comment)

    return templates.TemplateResponse(
        "comment.html",
        {"request": request, "comments": comments},
    )

@app.delete("/comments")
def clear_comments():
    comments.clear()
    return {"status": "cleared"}
