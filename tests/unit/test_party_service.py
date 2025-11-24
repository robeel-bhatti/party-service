import pytest
from redis.exceptions import RedisError
from src.config.enums import ServiceEntities


def test_add_party_with_new_address(
    party_service,
    mock_uow,
    mock_cache_repository,
    post_payload,
    party_response,
    mock_address,
    mock_party,
    mock_party_history,
    mock_mappers,
):
    mock_uow.address_repository.get_by_hash.return_value = None
    mock_mappers.to_address.return_value = mock_address
    mock_mappers.to_party.return_value = mock_party
    mock_mappers.to_party_history.return_value = mock_party_history
    mock_mappers.to_party_response.return_value = party_response

    result = party_service.add_party(post_payload)

    assert result == party_response.to_dict()
    assert mock_party.address_id == mock_address.id
    assert mock_party_history.party_id == mock_party.id
    assert mock_uow.flush.call_count == 3

    mock_uow.__enter__.assert_called_once()
    mock_uow.__exit__.assert_called_once()
    mock_uow.address_repository.add.assert_called_once_with(mock_address)
    mock_uow.party_repository.add.assert_called_once_with(mock_party)
    mock_uow.party_history_repository.add.assert_called_once_with(mock_party_history)
    mock_cache_repository.add.assert_called_once_with(
        mock_party.id, ServiceEntities.PARTY, party_response.to_dict()
    )


def test_add_party_with_existing_address(
    party_service,
    mock_uow,
    mock_cache_repository,
    post_payload,
    party_response,
    mock_address,
    mock_party,
    mock_party_history,
    mock_mappers,
):
    mock_uow.address_repository.get_by_hash.return_value = mock_address
    mock_mappers.to_party.return_value = mock_party
    mock_mappers.to_party_history.return_value = mock_party_history
    mock_mappers.to_party_response.return_value = party_response

    result = party_service.add_party(post_payload)
    assert result == party_response.to_dict()
    assert mock_party.address_id == mock_address.id
    assert mock_uow.flush.call_count == 2

    mock_uow.address_repository.add.assert_not_called()
    mock_mappers.to_address.assert_not_called()
    mock_uow.party_repository.add.assert_called_once_with(mock_party)


def test_add_party_cache_failure(
    mocker,
    party_service,
    mock_uow,
    mock_cache_repository,
    post_payload,
    party_response,
    mock_address,
    mock_party,
    mock_party_history,
    mock_mappers,
):
    mock_logger = mocker.patch("src.service.party_service.logger")
    mock_uow.address_repository.get_by_hash.return_value = mock_address
    mock_mappers.to_party.return_value = mock_party
    mock_mappers.to_party_history.return_value = mock_party_history
    mock_mappers.to_party_response.return_value = party_response
    mock_cache_repository.add.side_effect = RedisError("Cache connection failed")

    result = party_service.add_party(post_payload)

    assert result == party_response.to_dict()
    mock_uow.party_repository.add.assert_called_once()

    mock_logger.warning.assert_called_once()
    warning_message = mock_logger.warning.call_args[0][0]
    assert "Error caching Party" in warning_message
    assert str(mock_party.id) in warning_message


def test_add_party_transaction_rollback_on_error(
    mocker,
    party_service,
    mock_uow,
    post_payload,
    mock_address,
    mock_party,
    mock_mappers,
):
    mock_uow.__exit__ = mocker.MagicMock(return_value=False)
    mock_uow.address_repository.get_by_hash.return_value = mock_address
    mock_mappers.to_party.return_value = mock_party
    mock_uow.party_repository.add.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        party_service.add_party(post_payload)

    mock_uow.__enter__.assert_called_once()
    mock_uow.__exit__.assert_called_once()
