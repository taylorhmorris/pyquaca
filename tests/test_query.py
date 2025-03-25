"""Tests for the Query class."""

from unittest import mock

from pyquaca.query import Query


def test_query_can_instantiate() -> None:
    """Test that the Query class can be instantiated."""

    query = Query("localhost")
    assert isinstance(query, Query)


# test retrieve_cache method is not called from query if check_cache is False
def test_retrieve_cache_not_called_if_check_cache_is_false() -> None:
    """Test that the retrieve_cache method is not called if check_cache is False."""

    mock_requester = mock.MagicMock()
    mock_requester.request = mock.MagicMock()
    mock_cache = mock.MagicMock()
    config = {"check_cache": False, "cache": mock_cache, "requester": mock_requester}
    query = Query("localhost", config)
    query.query("test")
    assert mock_cache.called is False
    assert mock_requester.request.called is True


# test retrieve_cache method is called from query if check_cache is True
def test_retrieve_cache_called_if_check_cache_is_true() -> None:
    """Test that the retrieve_cache method is called if check_cache is True."""

    mock_requester = mock.MagicMock()
    mock_requester.request = mock.MagicMock()
    mock_cache = mock.MagicMock()
    mock_cache.retrieve = mock.MagicMock()
    config = {"check_cache": True, "cache": mock_cache, "requester": mock_requester}
    query = Query("localhost", config)
    query.query("test")
    assert mock_cache.retrieve.called is True
    assert mock_requester.called is False


# Test that query calls parser if parser is present
def test_query_calls_parser_if_parser_is_present() -> None:
    """Test that the query calls the parser if the parser is present."""

    mock_response = mock.MagicMock()
    mock_response.status_code = 200
    mock_requester = mock.MagicMock()
    mock_requester.request = mock.MagicMock()
    mock_requester.request.return_value = mock_response
    mock_parser = mock.MagicMock()
    mock_parser.parse = mock.MagicMock()
    config = {"check_cache": False, "parser": mock_parser, "requester": mock_requester}
    query = Query("localhost", config)
    query.query("test")
    assert mock_parser.parse.called is True
    assert mock_requester.request.called is True
    assert mock_parser.parse.call_count == 1
    assert mock_requester.request.call_count == 1


# Test query when query string is not found in cache
def test_query_when_query_string_not_found_in_cache() -> None:
    """Test the query method when the query string is not found in the cache."""

    mock_cache = mock.MagicMock()
    mock_cache.retrieve = mock.MagicMock(return_value=None)
    mock_response = mock.MagicMock()
    mock_response.status_code = 200
    mock_requester = mock.MagicMock()
    mock_requester.request = mock.MagicMock()
    mock_requester.request.return_value = mock_response
    config = {"check_cache": True, "cache": mock_cache, "requester": mock_requester}
    query = Query("localhost", config)
    query.query("test")
    assert mock_cache.retrieve.called is True
    assert mock_requester.request.called is True
    assert mock_cache.retrieve.call_count == 1
    assert mock_requester.request.call_count == 1


# Test query when a new request is made without a parser, but cache is on
def test_query_when_new_request_made_without_parser_but_cache_is_on() -> None:
    """Test the query method when a new request is made with cache and no parser."""

    mock_cache = mock.MagicMock()
    mock_cache.retrieve = mock.MagicMock(return_value=None)
    mock_cache.store = mock.MagicMock()
    mock_response = mock.MagicMock()
    mock_response.status_code = 200
    mock_requester = mock.MagicMock()
    mock_requester.request = mock.MagicMock()
    mock_requester.request.return_value = mock_response

    config = {
        "check_cache": True,
        "cache": mock_cache,
        "requester": mock_requester,
    }
    query = Query(
        "localhost",
        config,
    )
    query.query("test")

    assert mock_cache.retrieve.called is True
    assert mock_requester.request.called is True
    assert mock_cache.retrieve.call_count == 1
    assert mock_requester.request.call_count == 1
    assert mock_cache.store.called is True
    assert mock_cache.store.call_count == 1
