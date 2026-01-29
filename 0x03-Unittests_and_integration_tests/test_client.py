#!/usr/bin/env python3
"""Unit tests for client.py"""

import unittest
from unittest.mock import patch
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @patch("client.get_json")
    def test_org(self, mock_get_json):
        """Test that org property returns correct payload"""
        mock_get_json.return_value = TEST_PAYLOAD[0][0]
        client = GithubOrgClient("google")
        self.assertEqual(client.org, TEST_PAYLOAD[0][0])
        mock_get_json.assert_called_once_with("https://api.github.com/orgs/google")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns repository names"""
        mock_get_json.return_value = TEST_PAYLOAD[0]
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), ["repo1", "repo2"])
        mock_get_json.assert_called()

    def test_has_license(self):
        """Test has_license static method"""
        repo = {"license": {"key": "apache-2.0"}}
        self.assertTrue(GithubOrgClient.has_license(repo, "apache-2.0"))
        self.assertFalse(GithubOrgClient.has_license(repo, "mit"))


if __name__ == "__main__":
    unittest.main()
