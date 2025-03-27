"""Parser for parsing query responses before storing in cache."""

import logging
from typing import Any, Protocol


class SupportsChain(Protocol):  # pylint: disable=too-few-public-methods
    """Protocol for chaining parsers."""

    def chain(self, parser: "SupportsParse") -> Any:
        """Chain a parser to this parser."""


class SupportsParse(Protocol):  # pylint: disable=too-few-public-methods
    """Protocol for parsing data."""

    def parse(self, raw: Any) -> Any:
        """Parse the raw data and return the parsed data."""


class SupportsParseChain(SupportsParse, SupportsChain, Protocol):
    """Protocol for parsers that support chaining."""


class Parser:
    """
    Parser for parsing query responses before storing in cache.

    - chain(parser) method is used to chain parsers together.
    - parse(raw) method is used to parse the raw data and return the parsed data.
      This method should be overridden by subclasses to implement parsing logic.
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger("Parser")
        self.next_parser: SupportsParseChain | None = None

    def chain(self, parser: SupportsParseChain) -> None:
        """
        Chain a parser to this parser.

        Args:
            parser: The parser to chain.

        Returns:
            The chained parser.
        """
        self.next_parser = parser

    def parse(self, raw: Any) -> Any:
        """
        Parse the raw data and return the parsed data.

        Args:
            raw: The raw data to parse.

        Returns:
            The parsed data.
        """
        if self.next_parser:
            return self.next_parser.parse(raw)
        return raw
