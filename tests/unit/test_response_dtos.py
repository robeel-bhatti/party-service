from datetime import datetime


def test_party_response_creation(party_response, address_response, meta_response):
    """Test that PartyResponse can be created with all fields"""
    assert party_response.id == 1
    assert party_response.first_name == "John"
    assert party_response.middle_name == "A."
    assert party_response.last_name == "Doe"
    assert party_response.email == "john.doe@example.com"
    assert party_response.phone_number == "5551234567"
    assert party_response.address.id == 1
    assert party_response.address.street_one == "123 Main St"
    assert party_response.address.street_two == "Apt 4B"
    assert party_response.address.city == "Springfield"
    assert party_response.address.state == "IL"
    assert party_response.address.postal_code == "62704"
    assert party_response.address.country == "USA"
    assert party_response.meta.created_by == "test.user"
    assert party_response.meta.updated_by == "test.user"
    assert isinstance(party_response.meta.created_at, datetime)
    assert isinstance(party_response.meta.updated_at, datetime)


def test_to_dict_structure(party_response):
    """Test that to_dict returns proper dictionary structure"""
    result = party_response.to_dict()
    assert isinstance(result, dict)
    assert result["id"] == 1
    assert result["firstName"] == "John"
    assert result["middleName"] == "A."
    assert result["lastName"] == "Doe"
    assert result["email"] == "john.doe@example.com"
    assert result["phoneNumber"] == "5551234567"

    # Check nested address
    assert "address" in result
    assert isinstance(result["address"], dict)
    assert result["address"]["id"] == 1
    assert result["address"]["streetOne"] == "123 Main St"

    # Check nested meta in party
    assert "meta" in result
    assert isinstance(result["meta"], dict)
    assert result["meta"]["createdBy"] == "test.user"
    assert result["meta"]["createdAt"] == "2025-01-01T12:00:00"
    assert result["meta"]["updatedBy"] == "test.user"
    assert result["meta"]["updatedAt"] == "2025-01-01T12:00:00"
