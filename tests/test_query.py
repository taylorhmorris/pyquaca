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
