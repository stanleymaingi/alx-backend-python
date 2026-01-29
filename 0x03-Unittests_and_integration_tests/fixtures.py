org_payload = {"login": "google", "repos_url": "http://fakeurl.com/repos"}

repos_payload = [
    {"name": "repo1", "license": {"key": "apache-2.0"}},
    {"name": "repo2", "license": {"key": "mit"}},
    {"name": "repo3", "license": {"key": "apache-2.0"}}
]

expected_repos = ["repo1", "repo2", "repo3"]

apache2_repos = ["repo1", "repo3"]
