from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sanitizer import sanitize_html

app = FastAPI(title="CWE-79 Lab: Build Your Own Sanitizer")

templates = Jinja2Templates(directory="templates")

# In-memory storage for comments (simulates a database)
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
    Process user comments with sanitization.
    
    This uses YOUR sanitize_html() function from sanitizer.py
    If your sanitizer works correctly, XSS attacks will be prevented!
    """
    # Use the student's sanitizer
    sanitized_comment = sanitize_html(comment)
    
    # Store the sanitized comment
    comments_db.append(sanitized_comment)
    
    return templates.TemplateResponse(
        "comment.html",
        {"request": request, "comments": comments_db}
    )

@app.delete("/comments")
def clear_comments():
    """Helper endpoint to clear all comments (for testing)"""
    comments_db.clear()
    return {"message": "All comments cleared"}
