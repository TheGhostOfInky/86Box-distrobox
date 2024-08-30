#!/bin/env sh

if ! command -v podman &> /dev/null
then
    echo "podman could not be found, install it with your package manager"
    exit 1
fi

if ! command -v podman-compose &> /dev/null
then
    echo "podman-compose could not be found, install it with your package manager"
    exit 1
fi

if ! command -v distrobox &> /dev/null
then
    echo "distrobox could not be found, install it with your package manager"
    exit 1
fi

podman container rm -f -i -v --filter "ancestor=localhost/86box-distrobox_custom"

podman image rm -f -i  localhost/86box-distrobox_custom 

podman-compose up

distrobox assemble create

distrobox enter 86box -- /usr/bin/86Box -R /var/86Box-roms