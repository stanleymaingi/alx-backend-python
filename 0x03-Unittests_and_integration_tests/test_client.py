#!/usr/bin/env python3
"""
Unit and integration tests for client.GithubOrgClient class.
"""
import unittest
import fixtures
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient



class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that org property returns correct data with mocked get_json."""
        mock_get_json.return_value = {"login": org_name, "id": 123}
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {"login": org_name, "id": 123})
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """Unit test _public_repos_url property."""
        client = GithubOrgClient("test_org")
        expected_url = "https://api.github.com/orgs/test_org/repos"

        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": expected_url}
            self.assertEqual(client._public_repos_url, expected_url)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Unit test public_repos method."""
        client = GithubOrgClient("test_org")
        repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        expected = ["repo1", "repo2", "repo3"]

        with patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://fakeurl.com/repos"
            mock_get_json.return_value = repos_payload

            self.assertEqual(client.public_repos(), expected)
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://fakeurl.com/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Unit test has_license method."""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [
        (fixtures.org_payload, fixtures.repos_payload,
         fixtures.expected_repos, fixtures.apache2_repos)
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos using real-ish data."""

    @classmethod
    def setUpClass(cls):
        """Set up patcher for requests.get before running tests."""
        cls.get_patcher = patch("client.requests.get")
        cls.mock_get = cls.get_patcher.start()

        def get_json_side_effect(url, *args, **kwargs):
            if url == cls.org_payload["repos_url"]:
                return cls.repos_payload
            return cls.org_payload

        cls.mock_get.return_value.json.side_effect = get_json_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns all repo names correctly."""
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with license filter."""
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )