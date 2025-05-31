#!/usr/bin/env python3
"""Test suite for GithubOrgClient.org"""

from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from typing import Callable, Mapping
from fixtures import TEST_PAYLOAD
from unittest.mock import patch, PropertyMock
import unittest

class TestGithubOrgClient(unittest.TestCase):
    """ Class to test GithubOrgClient model """
    
    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected, mock_get_json):
        mock_get_json.return_value = expected
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
