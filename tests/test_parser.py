from query_and_cache.parser import Parser


def test_parser_has_parse_method():
    parser = Parser()
    assert hasattr(parser, "parse")
    assert callable(getattr(parser, "parse"))
