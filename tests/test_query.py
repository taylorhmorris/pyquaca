"""Tests for the Query class."""

from unittest import mock

from query_and_cache.query import Query


def test_query_can_instantiate():
    """Test that the Query class can be instantiated."""

    query = Query("localhost")
    assert isinstance(query, Query)


def test_retrieve_cache_returns_false_with_empty_search_string():
    """Test that the retrieve_cache method returns False with an empty search string."""

    query = Query("localhost")
    result = query.retrieve_cache("")
    assert result is False


@mock.patch("query_and_cache.query.retrieve_from_cache", return_value=True)
def test_retrieve_from_cache_calls_retrieve_from_cache(mock_rfc):
    """Test that the retrieve_cache method calls the retrieve_from_cache function."""

    query = Query("localhost")
    result = query.retrieve_cache("test")
    assert result is True
    assert mock_rfc.called is True


# test store_in_cache method calls store_in_cache function
@mock.patch("query_and_cache.query.store_in_cache", return_value=True)
def test_store_in_cache_calls_store_in_cache(mock_sic):
    """Test that the store_in_cache method calls the store_in_cache function."""

    query = Query("localhost")
    result = query.store_in_cache("test", {"test": "data"})
    assert result is True
    assert mock_sic.called is True


# test store_in_cache method returns False with empty search string
def test_store_in_cache_returns_false_with_empty_search_string():
    """Test that the store_in_cache method returns False with an empty search string."""

    query = Query("localhost")
    result = query.store_in_cache("", {"test": "data"})
    assert result is False


# test store_in_cache method returns True with valid input
@mock.patch("query_and_cache.query.store_in_cache", return_value=True)
def test_store_in_cache_returns_true_with_valid_input(mock_sic):
    """Test that the store_in_cache method returns True with valid input."""

    query = Query("localhost")
    result = query.store_in_cache("test", {"test": "data"})
    assert result is True
    assert mock_sic.called is True


# test store_in_cache method updates word if data contains 'word' key
@mock.patch("query_and_cache.query.store_in_cache", return_value=True)
def test_store_in_cache_updates_word_if_data_contains_word_key(mock_sic):
    """Test that store_in_cache method updates word if data contains a 'word' key."""

    query = Query("localhost")
    result = query.store_in_cache("test", {"word": "newsearch"})
    assert result is True
    assert mock_sic.called is True
    assert mock_sic.call_args[0][1]["word"] == "newsearch"


# test retrieve_cache method is not called from query if check_cache is False
@mock.patch("query_and_cache.query.retrieve_or_request", return_value="<html></html>")
@mock.patch("query_and_cache.query.retrieve_from_cache", return_value=True)
def test_retrieve_cache_not_called_if_check_cache_is_false(mock_rfc, mock_ror):
    """Test that the retrieve_cache method is not called if check_cache is False."""

    query = Query("localhost", {"check_cache": False})
    try:
        query.query("test")
        assert False
    except NotImplementedError:
        assert True
    assert mock_rfc.called is False
    assert mock_ror.called is True


# test retrieve_cache method is called from query if check_cache is True
@mock.patch("query_and_cache.query.retrieve_or_request", return_value="<html></html>")
@mock.patch("query_and_cache.query.retrieve_from_cache", return_value="<html></html>")
def test_retrieve_cache_called_if_check_cache_is_true(mock_rfc, mock_ror):
    """Test that the retrieve_cache method is called if check_cache is True."""

    query = Query("localhost", {"check_cache": True})
    try:
        query.query("test")
        assert False
    except NotImplementedError:
        assert True
    assert mock_rfc.called is True
    assert mock_ror.called is False
