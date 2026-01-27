# cwe-20-input-validation/tests/test_validation.py
import pytest
from validator import validate_and_normalize

def test_reject_non_object_body():
    with pytest.raises(ValueError):
        validate_and_normalize(["not", "a", "dict"])

def test_q_must_be_string_and_bounded():
    with pytest.raises(ValueError):
        validate_and_normalize({"q": 123})
    with pytest.raises(ValueError):
        validate_and_normalize({"q": "a" * 5000})  # too long

def test_page_and_page_size_bounds():
    with pytest.raises(ValueError):
        validate_and_normalize({"page": 0})
    with pytest.raises(ValueError):
        validate_and_normalize({"page_size": 100000})  # availability risk

def test_sort_must_be_allowlisted():
    with pytest.raises(ValueError):
        validate_and_normalize({"sort": "-drop_table"})

def test_fields_must_be_allowlisted():
    with pytest.raises(ValueError):
        validate_and_normalize({"fields": []})
    with pytest.raises(ValueError):
        validate_and_normalize({"fields": ["password_hash"]})

def test_levels_must_be_allowlisted():
    with pytest.raises(ValueError):
        validate_and_normalize({"filters": {"level": ["INFO", "HACK"]}})
