Build docker image
```
docker build -t ros2_gazebo_cuda_img -f ros2_gazebo.Dockerfile .
```

Start docker container
```
docker run --rm -it \
    --name ros2_gazebo_cuda_ctn \
    --env="DISPLAY=$DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --net=host \
    --gpus=all \
    --shm-size 8G \
    --volume="$PWD:/workspace/" \
    -w /workspace/ \
    ros2_gazebo_cuda_img:latest /bin/bash
```

Inside docker, activate
```
source /opt/ros/jazzy/setup.bash
```

Open other terminal
```
docker ps | grep "ros2_gazebo_cuda_ctn" | awk '{ print $1 }' | xargs -I {} sh -c "xhost +local:{}"
```