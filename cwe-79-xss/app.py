from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sanitizer import sanitize_html

app = FastAPI(title="CWE-79 XSS Lab")

templates = Jinja2Templates(directory="templates")

# In-memory storage for comments
comments_db = []

@app.get("/comment", response_class=HTMLResponse)
def show_form(request: Request):
    return templates.TemplateResponse(
        "comment.html",
        {"request": request, "comments": comments_db}
    )

@app.post("/comment", response_class=HTMLResponse)
def submit_comment(request: Request, comment: str = Form(...)):
    # Sanitize the user input
    sanitized_comment = sanitize_html(comment)
    
    # Store the sanitized comment
    comments_db.append(sanitized_comment)
    
    return templates.TemplateResponse(
        "comment.html",
        {"request": request, "comments": comments_db}
    )

@app.delete("/comments")
def clear_comments():
    comments_db.clear()
    return {"message": "All comments cleared"}
