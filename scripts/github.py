from github_types import CommitList, Runs
from typing import cast
import requests


class GithubRepo:
    COMMIT_DEFAULT = 30
    owner: str
    repo: str
    session: requests.Session

    def __init__(self, owner: str, repo: str) -> None:
        self.owner = owner
        self.repo = repo
        self.session = requests.Session()

    def __get_response(self, endpoint: str, query: dict[str, str] = {}) -> object:
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/{endpoint}"
        resp = self.session.get(url, params=query)

        if resp.status_code >= 300:
            raise Exception(f"Got response code {resp.status_code}: {resp.text}")

        c_type = resp.headers.get("Content-Type")
        if c_type is None or not c_type.lower().startswith("application/json"):
            raise Exception(f"Got response with content-type {c_type}, expected application/json")

        return resp.json()

    def get_commits(self, count: int = COMMIT_DEFAULT):
        try:
            return cast(CommitList, self.__get_response(
                "commits", {"per_page": str(count)}
            ))

        except Exception as e:
            raise Exception(
                f"Failed to get the latest {count} commit(s) for repo {self.owner}/{self.repo}"
            ) from e

    def __get_runs(self, sha: str) -> Runs:
        try:
            return cast(Runs, self.__get_response("actions/runs", {
                "head_sha": sha,
                "per_page": "100"
            }))

        except Exception as e:
            raise Exception(f"Failed to get action runs for commit {sha}") from e

    def get_status(self, sha: str) -> bool:
        KEYS = ["CMake (Linux)", "CodeQL Analysis (Linux)"]
        runs = self.__get_runs(sha)["workflow_runs"]
        key_status = [
            (run["status"], run["conclusion"]) for run in runs if run["name"] in KEYS
        ]

        if len(key_status) < len(KEYS):
            return False

        return all([
            status == "completed" and conclusion == "success" for
            status, conclusion in key_status
        ])

    def get_last_sucess(self) -> str:
        commits = self.get_commits()
        for commit in commits:
            sha = commit["sha"]
            if self.get_status(sha):
                return sha

        raise Exception("No sucessfully built commit found in the provided range")

    def get_tarball(self, sha: str) -> str:
        base_url = f"https://github.com/{self.owner}/{self.repo}/archive"
        return f"{base_url}/{sha}.tar.gz"
