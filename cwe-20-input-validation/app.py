from fastapi import FastAPI, HTTPException
from validator import validate_and_normalize

app = FastAPI(title="CWE-20 Lab: Improper Input Validation")

DATA = [
    {"id": 1, "service": "api", "level": "INFO", "timestamp": "2026-01-20T10:00:00Z", "message": "started"},
    {"id": 2, "service": "worker", "level": "WARN", "timestamp": "2026-01-21T11:00:00Z", "message": "slow job"},
    {"id": 3, "service": "api", "level": "ERROR", "timestamp": "2026-01-22T12:00:00Z", "message": "timeout"},
    {"id": 4, "service": "worker", "level": "WARN", "timestamp": "2026-01-22T12:00:00Z", "message": "fast job"},
]

@app.post("/search")
def search(payload: dict):
    try:
        norm = validate_and_normalize(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    q = norm["q"]
    service = norm["filters"]["service"]
    levels = set(norm["filters"]["level"])
    fields = norm["fields"]
    sort = norm["sort"]
    page = norm["page"]
    page_size = norm["page_size"]

    rows = []
    for r in DATA:
        if service and r["service"] != service:
            continue
        if levels and r["level"] not in levels:
            continue
        if q and q.lower() not in r["message"].lower():
            continue
        rows.append(r)

    reverse = sort.startswith("-")
    key = sort.lstrip("-")
    rows.sort(key=lambda x: x.get(key, ""), reverse=reverse)

    start = (page - 1) * page_size
    end = start + page_size
    page_rows = rows[start:end]

    result = [{k: row.get(k) for k in fields} for row in page_rows]
    return {"count": len(rows), "results": result}
