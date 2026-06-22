Start with docker 
```
docker run --rm -it \
    --device /dev/dri:/dev/dri \
    --gpus all \
    -e DISPLAY=$DISPLAY \
    -e NVIDIA_VISIBLE_DEVICES=all \
    -e NVIDIA_DRIVER_CAPABILITIES=all,graphics,display,utility \
    -e __NV_PRIME_RENDER_OFFLOAD=1 \
    -e __GLX_VENDOR_LIBRARY_NAME=nvidia \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    cyberbotics/webots:latest
```