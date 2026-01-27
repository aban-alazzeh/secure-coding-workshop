ALLOWED_LEVELS = {"INFO", "WARN", "ERROR"}
ALLOWED_SORT_FIELDS = {"timestamp", "level", "service", "id"}
ALLOWED_FIELDS = {"id", "service", "level", "timestamp", "message"}

def validate_and_normalize(payload: dict) -> dict:
    """
    INTENTIONALLY INSECURE (CWE-20).
    Attendees must harden this function until tests pass.
    """
    if not isinstance(payload, dict):
        raise ValueError("Invalid request body")

    q = payload.get("q", "")
    filters = payload.get("filters", {}) or {}
    sort = payload.get("sort", "-timestamp")
    page = payload.get("page", 1)
    page_size = payload.get("page_size", 50)
    fields = payload.get("fields", ["id", "timestamp", "message"])

    service = filters.get("service")
    level = filters.get("level", ["INFO", "WARN", "ERROR"])

    return {
        "q": q,
        "filters": {
            "service": service,
            "level": level,
        },
        "sort": sort,
        "page": page,
        "page_size": page_size,
        "fields": fields,
    }
