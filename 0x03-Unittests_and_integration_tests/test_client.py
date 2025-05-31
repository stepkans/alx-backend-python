#!/usr/bin/env python3
""" Model for client model methods """
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from typing import Callable, Mapping
from fixtures import TEST_PAYLOAD
from unittest.mock import patch, PropertyMock
import unittest
import utils
import fixtures
import client


class TestGithubOrgClient(unittest.TestCase):
    """ Class to test GithubOrgClient model """

    @parameterized.expand([
        ("google", {"payload": True}),
        ("abc", {"payload": False}),
    ])
    @patch("client.get_json")
    def test_org(self, org_name: str, result: Mapping, mock_get_jsn: Callable):
        """test that GithubOrgClient.org returns the correct value."""
        mock_get_jsn.return_value = result
        git_hub_org = GithubOrgClient(org_name)
        resp = git_hub_org.org
        self.assertEqual(result, resp)
        resp = git_hub_org.org
        mock_get_jsn.assert_called_once()

    @parameterized.expand([
        ("google", {"repos_url": "https://api.github.com/orgs/google"}),
        ("abc", {"repos_url": "https://api.github.com/orgs/abc"})
    ])
    def test_public_repos_url(self, org_name: str, result: Mapping):
        """Test that the result of _public_repos_url is the expected
        one based on the mocked payload."""
        with patch.object(GithubOrgClient, "org",
                          new_callable=PropertyMock) as mock_org:
            mock_org.return_value = result
            git_hub_org = GithubOrgClient(org_name)
            resp = git_hub_org._public_repos_url
            self.assertEqual(result["repos_url"], resp)

    @patch("client.get_json", return_value=[{"name": "alx"}])
    def test_public_repos(self, mock_get_json: Callable):
        """test that GithubOrgClient.public_repos returns correct value."""
        with patch.object(GithubOrgClient, "_public_repos_url",
                          return_value="https://api.github.com/orgs/abc",
                          new_callable=PropertyMock) as mock_public_repos_url:
            git_hub_org = GithubOrgClient("alx")
            resp = git_hub_org.public_repos()
            self.assertEqual(resp, ["alx"])
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo: Mapping, license_key: str, result: bool):
        """ Test that the result of has_license is the expected result """
        res = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(res, result)


@parameterized_class(('org_payload', 'repos_payload', 'expected_repos',
                      'apache2_repos'), TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Test the GithubOrgClient.public_repos method in an integration test."""

    @classmethod
    def setUpClass(self):
        """ Set up elements """
        self.get_patcher = patch("requests.get")
        self.mock_patcher = self.get_patcher.start()
        self.mock_json = self.mock_patcher.return_value

        def side_effect(args):
            if args == "https://api.github.com/orgs/google":
                self.mock_json.json.return_value = self.org_payload
                return self.mock_patcher.return_value
            elif args == "https://api.github.com/orgs/google/repos":
                self.mock_json.json.return_value = self.repos_payload
                return self.mock_patcher.return_value
        self.mock_patcher.side_effect = side_effect

    @classmethod
    def tearDownClass(self):
        """ Tear down elements """
        self.get_patcher.stop()

    def test_public_repos(self):
        """Test the public_repos method with None license"""
        git_hub_org = GithubOrgClient("google")
        result = git_hub_org.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test the public_repos method with license"""
        git_hub_org = GithubOrgClient("google")
        result = git_hub_org.public_repos("apache-2.0")
        self.assertEqual(result, self.apache2_repos)


class TestGithubOrgClient(unittest.TestCase):
    """Test the GithubOrgClient.public_repos method based on fixtures."""

    @patch('client.get_json')
    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos(self, mock_org, mock_get_json):
        """Test the public_repos method with mock"""
        # Fixtures
        repos_url = "http://api.github.com/orgs/test/repos"
        mock_org.return_value = {"repos_url": repos_url}
        payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = payload

        client = GithubOrgClient("test")
        self.assertEqual(client.public_repos(), ["repo1", "repo2", "repo3"])
        url = "http://api.github.com/orgs/test/repos"
        mock_get_json.assert_called_once_with(url)

    @patch('client.get_json')
    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_with_license(self, mock_org, mock_get_json):
        """Test the public_repos method with license & mock"""
        # Fixtures
        mock_org.return_value = {
            "repos_url": "http://api.github.com/orgs/test/repos"
        }
        payload = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
            {"name": "repo3", "license": None},
        ]
        mock_get_json.return_value = payload

        client = GithubOrgClient("test")
        self.assertEqual(client.public_repos(license="apache-2.0"), ["repo1"])


if __name__ == "__main__":
    unittest.main()
