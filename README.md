# 86Box-distrobox

This repository provides files for automatically pulling
the latest sucessful build of 86Box from github, compiling it
and running it inside a podman container using distrobox

# Requirements

This project has 3 requirements: podman, podman-compose and distrobox

Installing dependencies on `apt` based distros like Debian/Ubuntu/Mint:

```sh
sudo apt install podman podman-compose distrobox crun
```

Installing dependencies on `dnf` based distros like Fedora/RHEL/CentOS/Rocky/Alma:

```sh
sudo dnf install podman podman-compose distrobox
```

Installing dependencies on Arch-linux based distros (Manjaro/SteamOS):

```sh
sudo pacman -Syu podman podman-compose distrobox
```

# Running

The `run-all.sh` script will run all the necessary commands, 
alternatively you can run the following commands in the root
of this project:

```sh
podman-compose up
distrobox assemble create
distrobox enter 86box -- /usr/bin/86Box -R /var/86Box-roms
```

After the first 2 commands have been ran sucessfully you only need
to run the last one to start the machine, to stop it run:

```sh
distrobox stop 86box
```

# More information about this image

- This image uses the latest version of fedora stable, this is due to two
reasons: I'm familiar with fedora's packages and directories as it's
my primary distro and I find that it strikes a good balance of having
up-to-date packages while still keeping a passable level of stability.
If you wish to recreate this project using Ubuntu or another distro 
feel free, in principle all you'll have to edit is the install commands
in the Containerfile.

- It uses a pair of python scripts that call a minimal implementation
of a github API client, for obvious reasons they use the public API and
are therefore unauthenticated, so there's a high chance of being rate 
limited if you run the build script multiple times in quick sucession.
If you do get rate limited edit the `Containerfile` according to the
instructions provided in the comments, you can get the URLs for the 
harcoded tar.gz files from the github releases or the jenkins page.

- By default this image builds in `development` mode, which includes
experimental features not enabled for stable builds, if you wish to
get only the stable build's features pass a different `CMAKE_PRESET`
environment variable to `podman-compose` or the `run-all.sh`
script like this:

```sh
CMAKE_PRESET=regular ./run-all.sh
```
Other 86Box presets are also supported, the full table is available
at <https://86box.readthedocs.io/en/latest/dev/buildguide.html#presets>