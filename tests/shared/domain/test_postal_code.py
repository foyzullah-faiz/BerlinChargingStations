import pytest
from src.shared.domain.value_objects.PostalCode import PostalCode

def test_postal_code_valid():
    # Happy Path [cite: 83]
    zip_obj = PostalCode("10117")
    assert zip_obj.value == "10117"

def test_postal_code_invalid_length():
    # Error Scenario [cite: 83]
    with pytest.raises(ValueError, match="Invalid Berlin ZIP"):
        PostalCode("123")