"""Tests for the Parser class."""

from query_and_cache.parser import Parser


def test_parser_has_parse_method():
    """Test that the Parser class has a parse method."""
    parser = Parser()
    assert hasattr(parser, "parse")
    assert callable(getattr(parser, "parse"))
