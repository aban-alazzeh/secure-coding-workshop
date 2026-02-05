from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from validator import validate_and_calculate_total

app = FastAPI()
templates = Jinja2Templates(directory="templates")

ITEM_NAME = "Conference T-Shirt"
UNIT_PRICE = 15.00


@app.get("/", response_class=HTMLResponse)
def root():
    return RedirectResponse(url="/checkout", status_code=302)


@app.get("/checkout", response_class=HTMLResponse)
def checkout_page(request: Request):
    return templates.TemplateResponse(
        "checkout.html",
        {
            "request": request,
            "item_name": ITEM_NAME,
            "unit_price": UNIT_PRICE,
            "error": None,
            "quantity": "",
            "discount": "",
        },
    )


@app.post("/checkout", response_class=HTMLResponse)
def checkout_ui(request: Request, quantity: str = Form(None), discount: str = Form(None)):
    """
    UI route: shows receipt page on success.
    Shows an error message on the checkout page on invalid input.
    """
    result = validate_and_calculate_total(
        quantity=quantity,
        discount=discount,
        unit_price=UNIT_PRICE,
    )

    if not result["ok"]:
        return templates.TemplateResponse(
            "checkout.html",
            {
                "request": request,
                "item_name": ITEM_NAME,
                "unit_price": UNIT_PRICE,
                "error": result["error"],
                "quantity": quantity,
                "discount": discount,
            },
            status_code=400,
        )

    details = result["details"]
    return templates.TemplateResponse(
        "receipt.html",
        {
            "request": request,
            "item_name": ITEM_NAME,
            "unit_price": UNIT_PRICE,
            "quantity": details["quantity"],
            "discount": details["discount"],
            "total": result["total"],
        },
    )


@app.post("/api/checkout")
def checkout_api(quantity: str = Form(None), discount: str = Form(None)):
    """
    API route used by tests.
    Returns 400 + {"ok": false, "error": "..."} on invalid input.
    """
    result = validate_and_calculate_total(
        quantity=quantity,
        discount=discount,
        unit_price=UNIT_PRICE,
    )

    if not result["ok"]:
        return JSONResponse(status_code=400, content={"ok": False, "error": result["error"]})

    details = result["details"]
    return JSONResponse(
        status_code=200,
        content={
            "ok": True,
            "item": ITEM_NAME,
            "unit_price": UNIT_PRICE,
            "quantity": details["quantity"],
            "discount": details["discount"],
            "total": result["total"],
        },
    )
