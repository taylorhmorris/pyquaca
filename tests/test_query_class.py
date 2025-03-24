"""
Unit tests for the Query class in the query_and_cache.Query module.
"""

import unittest

from query_and_cache.query import Query


class Test(unittest.TestCase):
    """
    Test cases for the Query class.
    """

    def test_query_respects_params(self) -> None:
        """
        Test that the Query object correctly respects the parameters passed to it.
        """

        query = Query(
            "localhost",
            config={
                "auth": "auth_type",
                "check_cache": False,
                "api_key": "fakekey",
                "cache_path": "new_cache",
            },
        )
        self.assertEqual(query.url, "localhost")
        self.assertEqual(query.auth, "auth_type")
        self.assertEqual(query.check_cache, False)
        self.assertEqual(query.api_key, "fakekey")

    def test_query_has_cache_on_by_default(self) -> None:
        """
        Test that the Query object has caching enabled by default.
        """
        query = Query("localhost")
        self.assertEqual(query.check_cache, True)


if __name__ == "__main__":
    unittest.main()
