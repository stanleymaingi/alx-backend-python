import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": {"b": {"c": 1}}}, ("a", "b", "c"), 1),
        ({"a": 1}, ("a",), 1),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns expected value."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, missing_key):
        """Test access_nested_map raises KeyError with correct message."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{missing_key}'")


class TestGetJson(unittest.TestCase):
    @patch("utils.requests.get")
    def test_get_json(self, mock_get):
        """Test get_json returns expected payload and calls requests.get once."""
        test_cases = [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]

        for test_url, test_payload in test_cases:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            result = get_json(test_url)

            # Ensure requests.get was called exactly once with test_url
            mock_get.assert_called_once_with(test_url)
            # Ensure returned payload is correct
            self.assertEqual(result, test_payload)

            # Reset mock for next iteration
            mock_get.reset_mock()


class TestMemoize(unittest.TestCase):
    class TestClass:
        def __init__(self):
            self.calls = 0

        @memoize
        def method(self):
            self.calls += 1
            return 42

    def test_memoize(self):
        """Test that memoize caches the method call."""
        obj = self.TestClass()
        obj.method()
        obj.method()
        self.assertEqual(obj.calls, 1)


if __name__ == "__main__":
    unittest.main()
