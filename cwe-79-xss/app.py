from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="CWE-79 Lab: Stored Cross-Site Scripting (XSS)")

templates = Jinja2Templates(directory="templates")

# In-memory storage for comments (simulates a database)
# In a real app, this would be a database table
comments_db = []

@app.get("/comment", response_class=HTMLResponse)
def show_form(request: Request):
    """Display the comment form and all stored comments"""
    return templates.TemplateResponse(
        "comment.html",
        {"request": request, "comments": comments_db}
    )

@app.post("/comment", response_class=HTMLResponse)
def submit_comment(request: Request, comment: str = Form(...)):
    """
    INTENTIONALLY VULNERABLE: 
    - User input is stored directly without sanitization
    - Template renders with | safe filter, executing any HTML/JS
    - This creates a STORED XSS vulnerability affecting all users
    """
    # Store the comment directly without any sanitization
    comments_db.append(comment)
    
    return templates.TemplateResponse(
        "comment.html",
        {"request": request, "comments": comments_db}
    )

@app.delete("/comments")
def clear_comments():
    """Helper endpoint to clear all comments (for testing)"""
    comments_db.clear()
    return {"message": "All comments cleared"}
