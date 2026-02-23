# Mujoco samples

## Install
Build docker image
```
docker build -t mujoco_gpu_img -f ./Dockerfile .
```

Start docker container
```
docker run --rm --name mujoco_gpu_ctn -it --network host --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 --gpus all  -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --volume="$PWD:/workspace" -w /workspace/ --device /dev/dri:/dev/dri mujoco_gpu_img bash
```

## References
https://github.com/HaoxiangYou/MujocoTutorials