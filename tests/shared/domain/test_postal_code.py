import pytest
from src.shared.domain.value_objects.PostalCode import PostalCode

def test_postal_code_validation_fails_on_wrong_length():
    # We expect a ValueError if the ZIP is not 5 digits
    with pytest.raises(ValueError, match="Invalid Berlin ZIP"):
        PostalCode("123")