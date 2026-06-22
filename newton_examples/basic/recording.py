import numpy as np
import warp as wp

import newton
import newton.examples

class Example:
    def __int__(self, viewer, _args):
        # Setup simulation parameters
        self.fps = 60
        self.frame_dt = 1.0 / self.fps
        self.sim_time = 0.0
        self.sim_substeps = 10
        self.sim_dt = self.frame_dt / self.sim_substeps

        self.viewer = viewer
        self.world_count = 100

        # Set numpy random seed for reproducibility
        self.seed = 123
        self.rng = np.random.default_rng(self.seed)

        start_rotation = wp.quat_from_axis_angle(wp.normalize(wp.vec3(*self.rng.uniform(-1.0, 1.0, size=3))), -wp.pi * 0.5)