from sys import stderr
from github import GithubRepo

try:
    main_repo = GithubRepo("86Box", "86Box")
    last_good = main_repo.get_last_sucess()
    tarball = main_repo.get_tarball(last_good)
    print(tarball)

except Exception as e:
    print(f"Failed to retrieve last good tarball due to error:", file=stderr)
    while e:
        print(e.__str__(), file=stderr)
        e = e.__cause__
    exit(0)
