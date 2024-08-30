FROM registry.fedoraproject.org/fedora:latest

ARG CMAKE_PRESET=development
ENV ROM_DIR /var/86Box-roms
ENV WORKING_DIR /temp/86Box

RUN echo $CMAKE_PRESET

RUN python3 -c "exit(1)"

RUN mkdir -p "$WORKING_DIR"

RUN dnf -y upgrade --refresh && \
    dnf -y groupinstall "C Development Tools and Libraries" && \
    dnf -y install \
        --setopt=install_weak_deps=False \
        #Ensure tar, wget, python3 and requests are installed (should always be but doesn't hurt)
        tar wget python3 python-requests \
        #86Box build dependencies
        cmake extra-cmake-modules pkg-config \
        ninja-build freetype-devel SDL2-devel \
        libatomic libpng-devel libslirp-devel \
        libXi-devel openal-soft-devel rtmidi-devel \
        fluidsynth-devel libsndfile-devel \
        qt5-linguist qt5-qtconfiguration-devel \
        qt5-qtbase-private-devel qt5-qtbase-static \
        wayland-devel libevdev-devel \
        libxkbcommon-x11-devel zlib-ng-compat-static

#Ensure python3 version is at least 3.12.0
RUN python3 -c "from sys import version_info as vi;exit(int(vi < (3,12,0)))"

#Ensure require packages are present
RUN python3 -c "import requests"

#Copies scripts to the /scripts directory on the image
COPY scripts scripts/

#Fetches and unpacks the latest working source code
RUN wget -O "$WORKING_DIR/86Box.tar.gz" `python3 /scripts/main.py`
#Replace with wget -O "$WORKING_DIR/86Box.tar.gz" "my-hardcoded-url" if it gets rate limited

RUN cd "$WORKING_DIR" && tar -xzf 86Box.tar.gz

RUN cd "$WORKING_DIR" && mv 86Box-* 86Box

#Fetches and unpacks the latest roms
RUN wget -O "$WORKING_DIR/roms.tar.gz" `python3 /scripts/roms.py`
#Replace with wget -O "$WORKING_DIR/roms.tar.gz" "my-hardcoded-url" if it gets rate limited

RUN cd "$WORKING_DIR" && tar -xzf roms.tar.gz

RUN cd "$WORKING_DIR" && mkdir /var/86Box-roms

RUN cd "$WORKING_DIR" && mv roms-*/* /var/86Box-roms

#Creates build dir and condigures CMake
RUN cd "$WORKING_DIR" && mkdir -p ./build

RUN cd "$WORKING_DIR" && cmake \
    -B "$WORKING_DIR/build" \
    -S "$WORKING_DIR/86Box" \
    --preset "$CMAKE_PRESET" \
    -D CMAKE_TOOLCHAIN_FILE="$WORKING_DIR/86Box/cmake/flags-gcc-x86_64.cmake"

#Compiles the previously configured CMake project
RUN cd "$WORKING_DIR" && cmake --build "$WORKING_DIR/build"

#Copies the 86Box executable to a location in $PATH to allow global execution
RUN cp "$WORKING_DIR/build/src/86Box" /usr/bin

#Cleans up Working directory
RUN rm -rf "$WORKING_DIR"