"""Tests for the Query class."""

from unittest import mock

from query_and_cache.query import Query


def test_query_can_instantiate() -> None:
    """Test that the Query class can be instantiated."""

    query = Query("localhost")
    assert isinstance(query, Query)


# test retrieve_cache method is not called from query if check_cache is False
@mock.patch("query_and_cache.query.requests.get")
def test_retrieve_cache_not_called_if_check_cache_is_false(mock_ror) -> None:
    """Test that the retrieve_cache method is not called if check_cache is False."""

    mock_rfc = mock.MagicMock()
    query = Query("localhost", {"check_cache": False, "cache": mock_rfc})
    query.query("test")
    assert mock_rfc.called is False
    assert mock_ror.called is True


# test retrieve_cache method is called from query if check_cache is True
@mock.patch("query_and_cache.query.requests.get")
def test_retrieve_cache_called_if_check_cache_is_true(mock_ror) -> None:
    """Test that the retrieve_cache method is called if check_cache is True."""

    mock_rfc = mock.MagicMock()
    mock_rfc.retrieve = mock.MagicMock()
    query = Query("localhost", {"check_cache": True, "cache": mock_rfc})
    query.query("test")
    assert mock_rfc.retrieve.called is True
    assert mock_ror.called is False
