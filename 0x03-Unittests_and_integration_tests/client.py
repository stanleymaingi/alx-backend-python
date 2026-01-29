#!/usr/bin/env python3
from typing import List
from utils import get_json, memoize


class GithubOrgClient:
    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name: str):
        self.org_name = org_name

    @property
    def org(self):
        return get_json(self.ORG_URL.format(self.org_name))

    @property
    def _public_repos_url(self):
        return self.org["repos_url"]

    @memoize
    def repos_payload(self):
        return get_json(self._public_repos_url)

    def public_repos(self, license=None) -> List[str]:
        repos = self.repos_payload()
        result = []
        for repo in repos:
            if license is None or self.has_license(repo, license):
                result.append(repo["name"])
        return result

    @staticmethod
    def has_license(repo, license_key):
        if repo.get("license") is None:
            return False
        return repo["license"].get("key") == license_key
