import mujoco
import mujoco.viewer
import time
import numpy as np

# 1. Define the model (Adding an actuator so we can move it)
xml = """
<mujoco>
  <worldbody>
    <light name="top" pos="0 0 1"/>
    <body name="box_and_sphere" euler="0 0 -30">
      <joint name="swing" type="hinge" axis="1 -1 0" pos="-.2 -.2 -.2"/>
      <geom name="red_box" type="box" size=".2 .2 .2" rgba="1 0 0 1"/>
      <geom name="green_sphere" pos=".2 .2 .2" size=".1" rgba="0 1 0 1"/>
    </body>
  </worldbody>
  
  <actuator>
    <motor name="swing_motor" joint="swing" gear="2"/>
  </actuator>
</mujoco>
"""

# 2. Load the model and create a data object
model = mujoco.MjModel.from_xml_string(xml)
data = mujoco.MjData(model)

# 3. Launch the passive viewer
with mujoco.viewer.launch_passive(model, data) as viewer:
    # Close the viewer automatically after 20 seconds
    start_time = time.time()
    
    while viewer.is_running() and (time.time() - start_time < 20):
        step_start = time.time()

        # 4. Apply a oscillating force (torque) to make it swing
        # We use a sine wave so it pushes back and forth
        torque = np.sin(data.time * 4) * 0.5
        data.ctrl[0] = torque

        # 5. Step the physics simulation
        mujoco.mj_step(model, data)

        # 6. Sync the viewer with the new physics state
        viewer.sync()

        # 7. Maintain real-time speed
        time_until_next_step = model.opt.timestep - (time.time() - step_start)
        if time_until_next_step > 0:
            time.sleep(time_until_next_step)