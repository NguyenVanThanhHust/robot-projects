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
    libx11-dev

WORKDIR /root/.mujoco
RUN wget https://github.com/deepmind/mujoco/releases/download/2.1.0/mujoco210-linux-x86_64.tar.gz && tar -xf mujoco210-linux-x86_64.tar.gz
RUN git clone https://github.com/openai/mujoco-py
WORKDIR /root/.mujoco/mujoco-py/
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/root/.mujoco/mujoco210/bin
RUN pip install "cython<3" && python setup.py develop
