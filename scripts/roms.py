from sys import stderr
from github import GithubRepo

try:
    roms_repo = GithubRepo("86Box", "roms")
    latest = roms_repo.get_commits(1)[0]
    tarball = roms_repo.get_tarball(latest["sha"])
    print(tarball)

except Exception as e:
    print(f"Failed to retrieve latest tarball due to error:", file=stderr)
    while e:
        print(e.__str__(), file=stderr)
        e = e.__cause__
    exit(0)
