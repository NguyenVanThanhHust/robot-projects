# https://gist.github.com/saratrajput/60b1310fe9d9df664f9983b38b50d5da
FROM pytorch/pytorch:2.9.0-cuda12.8-cudnn9-devel
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y software-properties-common wget curl
RUN add-apt-repository universe && apt update && apt-get install -y \
    libglfw3 \
    libglew2.2 \
    libgl1-mesa-glx \
    libosmesa6 \
    libglew-dev \
    git \
    libosmesa6-dev \
    cmake \
    g++ \
    libgl1-mesa-dev \
    libosmesa6-dev \
    libglew-dev \
    libglfw3-dev \
    libx11-dev

ENV MUJOCO_VERSION=3.5.0
WORKDIR /opt

RUN wget https://github.com/google-deepmind/mujoco/releases/download/${MUJOCO_VERSION}/mujoco-${MUJOCO_VERSION}-linux-x86_64.tar.gz \
    && mkdir -p mujoco \
    && tar -xzf mujoco-${MUJOCO_VERSION}-linux-x86_64.tar.gz -C mujoco --strip-components=1 \
    && rm mujoco-${MUJOCO_VERSION}-linux-x86_64.tar.gz

ENV MUJOCO_DIR=/opt/mujoco
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/mujoco/lib
ENV PATH=$PATH:/opt/mujoco/bin
RUN pip install jupyterlab mujoco "gymnasium[mujoco]" mediapy

ARG USERNAME=thanh
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# ********************************************************
# * Anything else you want to do like clean up goes here *
# ********************************************************

# [Optional] Set the default user. Omit if you want to keep the default as root.
USER $USERNAME

