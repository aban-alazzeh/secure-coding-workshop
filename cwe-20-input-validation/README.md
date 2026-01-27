# CWE-20: Improper Input Validation

This lab focuses on fixing improper input validation in a small, runnable API. The goal is to enforce clear input rules, bounds, and allowlists so the application behaves safely under normal and edge-case inputs. You will review the code, run failing tests, and update the validation logic to prevent downstream security and availability issues.

You are only allowed to modify `validator.py`. Do not change the tests and do not add new dependencies.

Setup instructions (run all commands from inside the `cwe-20-input-validation` directory):

Linux or macOS:
python3 -m venv .venv
source .venv/bin/activate

Windows PowerShell:
python -m venv .venv
.\.venv\Scripts\Activate.ps1

Windows cmd:
python -m venv .venv
.\.venv\Scripts\activate.bat

Install dependencies:
pip install -r requirements.txt

Run the tests (they are expected to fail at first):
pytest

Run the API:
uvicorn app:app --reload

Open your browser and go to:
http://127.0.0.1:8000/docs

Your task is to read `validator.py`, identify where input is accepted without proper validation, and implement strict validation and normalization inside `validate_and_normalize()`. When you are done, all tests should pass and invalid input should return HTTP 400 responses while valid input returns results.

You are finished when all tests pass, invalid input is rejected with safe error messages, and valid requests return search results.

You can use the built-in Swagger UI at `/docs` to send requests, or test with payloads such as these, which should be rejected after your fixes:

{ "q": "t", "page": 1, "page_size": 100000 }

{ "sort": "-drop_table" }

{ "fields": ["password_hash"] }

{ "filters": { "level": ["INFO", "HACK"] } }
