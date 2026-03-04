bulid docker image
```
docker build -t habitat_sim_img -f habitat.Dockerfile .
```

Start docker container
```
docker run --rm -it \
    --name habitat_sim_ctn \
    --env="DISPLAY=$DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --net=host \
    --gpus=all \
    --shm-size 8G \
    --volume="$PWD:/workspace/" \
    -w /workspace/ \
    habitat_sim_img:latest /bin/bash
```