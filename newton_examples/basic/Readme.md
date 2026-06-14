# Basic example of newton library

| File | Content | 
|---|---|
| basic_viewer.py | Shows how to use the Newton Viewer class to visualize various shapes and line instances without a Newton model. | 
| recording.py | Recording happens automatically - ViewerFile captures all logged states and saves them when the viewer is closed. | 


Here is the step-by-step summary of how you resolved the Segmentation Fault caused by the OpenGL handshake on your MSI Katana.

🛠️ Summary: Fixing NVIDIA OpenGL Crashes on Linux Laptops
The Problem: "Hybrid Graphics Conflict"
On laptops with both Intel (Integrated) and NVIDIA (Discrete) GPUs, the Wayland display server often tries to manage the "handover" of graphics tasks. When a high-performance library like Warp or Newton tries to create an OpenGL shader (glCreateShader), the driver crashes because it cannot navigate the "fence" Wayland puts between the two GPUs.

The Solution: Step-by-Step
1. Confirm the GPU is Healthy (Isolate Compute)
Before fixing the graphics, we verified that the NVIDIA card could perform math (Compute) without crashing.

Test: Run a simple Warp script without a GUI.

Lesson: If the math works but the window crashes, the problem is the Display Server (Wayland), not the hardware.

2. Disable Wayland and Switch to X11 (The "Magic" Fix)
Wayland is the modern default for Ubuntu, but it is often incompatible with specialized NVIDIA OpenGL tools. Switching to Xorg (X11) provides a direct path for the NVIDIA driver to control the screen.

Action: Edit /etc/gdm3/custom.conf and uncomment WaylandEnable=false.

Action: Reboot the system.

Verification: echo $XDG_SESSION_TYPE should return x11.

3. Sanitize the Library Path (LD_PRELOAD)
Python environments (Conda/Venv) often include their own versions of C++ and OpenGL libraries. These frequently conflict with the versions your NVIDIA driver expects.

Action: Use LD_PRELOAD to force the system's stable libraries to load first.

Key Libraries: /usr/lib/x86_64-linux-gnu/libstdc++.so.6 and libGL.so.1.

4. Disable Driver "Optimizations" that cause Race Conditions
NVIDIA drivers try to "thread" OpenGL calls and cache shaders on the disk to improve speed. On hybrid laptops, this often leads to permissions errors or memory corruption during startup.

Action: Set __GL_THREADED_OPTIMIZATIONS=0 and __GL_SHADER_DISK_CACHE=0.

5. Force NVIDIA Prime Offload
Since the Intel GPU still technically drives the laptop's physical screen, you must tell the system to "offload" the heavy rendering to the RTX 4060.

Action: Set __NV_PRIME_RENDER_OFFLOAD=1 and __GLX_VENDOR_LIBRARY_NAME=nvidia.