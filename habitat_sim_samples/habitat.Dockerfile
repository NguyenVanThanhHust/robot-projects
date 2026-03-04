FROM pytorch/pytorch:2.9.0-cuda12.8-cudnn9-devel

# Install packages without prompting the user to answer any questions
ENV DEBIAN_FRONTEND=noninteractive 

# Install packages
RUN apt-get update && apt-get install -y \
    locales \
    lsb-release \
    mesa-utils \
    git \
    subversion \
    nano \
    terminator \
    xterm \
    wget \
    curl \
    htop \
    libssl-dev \
    build-essential \
    dbus-x11 \
    software-properties-common \
    mesa-utils \
    libglu1-mesa-dev \
    freeglut3-dev \
    mesa-common-dev \
    gdb valgrind && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


WORKDIR /opt/
# Checkout the latest stable release
RUN git clone --branch stable https://github.com/facebookresearch/habitat-sim.git
WORKDIR /opt/habitat-sim
ENV CMAKE_ARGS="-DCMAKE_POLICY_VERSION_MINIMUM=3.5"
# RUN HABITAT_WITH_CUDA=ON pip install . --no-build-isolation
WORKDIR /workspace/