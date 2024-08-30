from typing import TypedDict, Any

type NOT_IMPLEMENTED = None | bool | str | int | float | \
    dict[str, NOT_IMPLEMENTED] | list[NOT_IMPLEMENTED]


class GitUser(TypedDict):
    name: str
    email: str
    date: str


class GithubUser(TypedDict):
    login: str
    id: int
    node_id: str
    avatar_url: str
    gravatar_id: str
    url: str
    html_url: str
    followers_url: str
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: str
    organizations_url: str
    repos_url: str
    events_url: str
    recieved_events_url: str
    type: str
    site_admin: bool


class CommitTree(TypedDict):
    sha: str
    url: str


class CommitInfo(TypedDict):
    author: GitUser
    committer: GitUser
    message: str
    tree: CommitTree
    url: str
    comment_count: int
    verification: NOT_IMPLEMENTED


class Commit(TypedDict):
    sha: str
    node_id: str
    commit: CommitInfo
    url: str
    html_url: str
    comments_url: str
    author: GithubUser
    committer: GithubUser
    parents: NOT_IMPLEMENTED


type CommitList = list[Commit]


class WorkflowRun(TypedDict):
    id: int
    name: str
    node_id: str
    head_branch: str
    head_sha: str
    path: str
    display_title: str
    run_number: int
    event: str
    status: str
    conclusion: str
    workflow_id: int
    check_suite_id: int
    check_suite_node_id: int
    url: str
    html_url: str
    pull_requests: NOT_IMPLEMENTED
    created_at: str
    updated_at: str
    actor: GithubUser
    run_attempt: int
    referenced_workflows: NOT_IMPLEMENTED
    triggering_actor: GithubUser
    jobs_url: str
    logs_url: str
    check_suite_url: str
    artifacts_url: str
    cancel_url: str
    rerun_url: str
    previous_attempt_url: None | str
    workflow_url: str
    head_commit: NOT_IMPLEMENTED
    repository: NOT_IMPLEMENTED
    head_repository: NOT_IMPLEMENTED


class Runs(TypedDict):
    total_count: int
    workflow_runs: list[WorkflowRun]
