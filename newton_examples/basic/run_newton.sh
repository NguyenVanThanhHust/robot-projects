#!/bin/bash
# 1. Extreme Library Sanitization
# We prioritize the system's core C and GL libraries over anything in miniconda3
export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6:/usr/lib/x86_64-linux-gnu/libgcc_s.so.1:/usr/lib/x86_64-linux-gnu/libGL.so.1:/usr/lib/x86_64-linux-gnu/libOpenGL.so.0

# 2. NVIDIA X11 Offload
export __NV_PRIME_RENDER_OFFLOAD=1
export __GLX_VENDOR_LIBRARY_NAME=nvidia

# 3. Disable internal Warp features that might conflict with the viewer
export WARP_DEVICE_MEMPOOL=0

# 4. Disable Shader Cache (Common fix for glCreateShader crash)
export __GL_SHADER_DISK_CACHE=0
export __GL_THREADED_OPTIMIZATIONS=0

# 5. Launch with absolute path to ensure no env-shuffling
echo "Launching Newton Viewer..."
python basic_viewer.py