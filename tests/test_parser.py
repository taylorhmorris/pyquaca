"""Tests for the Parser class."""

from query_and_cache.parser import Parser


def test_parser_has_parse_method():
    """Test that the Parser class has a parse method."""
    parser = Parser()
    assert hasattr(parser, "parse")
    assert callable(getattr(parser, "parse"))


def test_parser_chain_works():
    """Test that the Parser class can chain parsers."""
    parser = Parser()
    parser2 = Parser()
    parser2.parse = lambda x: x + "2"
    parser.chain(parser2)
    assert parser.next_parser == parser2
    result = parser.parse("test")
    assert result == "test2"


def test_parser_works():
    """Test that the Parser class works."""
    parser = Parser()
    result = parser.parse("test")
    assert result == "test"
