def _fail(msg: str):
    return {
        "ok": False,
        "error": msg,
        "total": None,
        "details": None,
    }


def _validate_quantity(raw: str):
    """
    Expected rules (NOT implemented yet):
    - Required
    - Digits only
    - Integer range: 1..20
    """
    # TODO: implement validation
    return None, None


def _validate_discount(raw: str):
    """
    Expected rules (NOT implemented yet):
    - Optional
    - Digits only if provided
    - Integer range: 0..50
    """
    # TODO: implement validation
    return 0, None


def validate_and_calculate_total(*, quantity: str, discount: str, unit_price: float):
    q, err = _validate_quantity(quantity)
    if err:
        return _fail(err)

    d, err = _validate_discount(discount)
    if err:
        return _fail(err)

    subtotal = q * float(unit_price)
    total = subtotal * (1.0 - (d / 100.0))

    return {
        "ok": True,
        "error": None,
        "total": total,
        "details": {"quantity": q, "discount": d},
    }
