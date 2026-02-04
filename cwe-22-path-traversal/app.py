from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="CWE-22 Path Traversal Lab")

BASE_DIR = Path(__file__).resolve().parent
REPORTS_DIR = BASE_DIR / "data" / "reports"

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    # Keep the UI simple and deterministic for the lab.
    # We only list known files to help users, but the vulnerability is in /report.
    try:
        report_names = sorted([p.name for p in REPORTS_DIR.iterdir() if p.is_file()])
    except Exception:
        report_names = []
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "report_names": report_names},
    )


@app.get("/report", response_class=HTMLResponse)
def view_report(request: Request, name: str = ""):
    """
    INTENTIONALLY VULNERABLE (CWE-22):
    The user controls 'name' and we join it directly to REPORTS_DIR.

    Example attack:
      /report?name=../secret.txt
    """
    content = ""
    error = None

    if not name:
        error = "Please provide a report name."
        return templates.TemplateResponse(
            "report.html",
            {"request": request, "name": name, "content": content, "error": error},
        )

    # ❌ Vulnerable path join: allows ../ traversal to escape REPORTS_DIR.
    target_path = REPORTS_DIR / name

    try:
        content = target_path.read_text(encoding="utf-8")
    except Exception:
        # Keep errors generic (matches your “don’t leak internals” style).
        error = "Report not found."

    return templates.TemplateResponse(
        "report.html",
        {"request": request, "name": name, "content": content, "error": error},
    )
