# cwe-20-input-validation/validator.py
ALLOWED_LEVELS = {"INFO", "WARN", "ERROR"}
ALLOWED_SORT_FIELDS = {"timestamp", "level", "service", "id"}
ALLOWED_FIELDS = {"id", "service", "level", "timestamp", "message"}

def validate_and_normalize(payload: dict) -> dict:
    """
    INTENTIONALLY INSECURE (CWE-20).
    Attendees will harden this function until tests pass.
    """
    if not isinstance(payload, dict):
        raise ValueError("Invalid request body")

    # Too-permissive defaults
    q = payload.get("q", "")
    filters = payload.get("filters", {}) or {}
    sort = payload.get("sort", "-timestamp")
    page = payload.get("page", 1)
    page_size = payload.get("page_size", 50)
    fields = payload.get("fields", ["id", "timestamp", "message"])

    # Too-permissive: no allowlists or normalization
    service = filters.get("service")
    level = filters.get("level", ["INFO", "WARN", "ERROR"])

    return {
        "q": q,
        "filters": {
            "service": service,
            "level": level,
            "from": filters.get("from"),
            "to": filters.get("to"),
        },
        "sort": sort,
        "page": page,
        "page_size": page_size,
        "fields": fields,
    }
