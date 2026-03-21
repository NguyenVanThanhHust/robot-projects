import math
import numpy as np
import warp as wp
from pxr import Usd, UsdGeom

import newton
import newton.examples

# 1. Initialize Warp and define the target device
wp.init()
device = wp.get_preferred_device()
print(f"Running Newton Example on device: {device}")

class Example:
    def __init__(self, viewer, args) -> None:
        self.viewer = viewer

        # Initialize arrays with explicit device targeting
        self.col_sphere = wp.array([wp.vec3(0.9, 0.1, 0.1)], dtype=wp.vec3, device=device)
        self.col_box = wp.array([wp.vec3(0.1, 0.9, 0.1)], dtype=wp.vec3, device=device)
        self.col_cone = wp.array([wp.vec3(0.1, 0.4, 0.9)], dtype=wp.vec3, device=device)
        self.col_capsule = wp.array([wp.vec3(0.9, 0.9, 0.1)], dtype=wp.vec3, device=device)
        self.col_cylinder = wp.array([wp.vec3(0.8, 0.5, 0.2)], dtype=wp.vec3, device=device)
        self.col_bunny = wp.array([wp.vec3(0.5, 0.2, 0.8)], dtype=wp.vec3, device=device)
        self.col_plane = wp.array([wp.vec3(0.125, 0.125, 0.15)], dtype=wp.vec3, device=device)

        self.mat_default = wp.array([wp.vec4(0.0, 0.7, 0.0, 0.0)], dtype=wp.vec4, device=device)
        self.mat_diffuse = wp.array([wp.vec4(0.8, 0.0, 1.0, 0.0)], dtype=wp.vec4, device=device)
        self.mat_plane = wp.array([wp.vec4(0.5, 0.5, 1.0, 0.0)], dtype=wp.vec4, device=device)

        # 2. Robust Mesh (Bunny) Loading
        self.bunny_mesh = None
        try:
            asset_path = newton.examples.get_asset("bunny.usd")
            print(f"Attempting to load: {asset_path}")
            usd_stage = Usd.Stage.Open(asset_path)
            
            if usd_stage:
                prim = usd_stage.GetPrimAtPath("/root/bunny")
                if prim.IsValid():
                    usd_geom = UsdGeom.Mesh(prim)
                    mesh_vertices = np.array(usd_geom.GetPointsAttr().Get())
                    mesh_indices = np.array(usd_geom.GetFaceVertexIndicesAttr().Get())
                    self.bunny_mesh = newton.Mesh(mesh_vertices, mesh_indices)
                    self.bunny_mesh.finalize()
                    print("Bunny mesh loaded successfully.")
                else:
                    print("Warning: Prim '/root/bunny' not found in USD file.")
            else:
                print("Warning: Failed to open USD stage.")
        except Exception as e:
            print(f"Mesh loading error: {e}")

        # 3. Debug Lines Setup
        axis_eps, axis_length = 0.01, 2.0
        self.axes_begins = wp.array([wp.vec3(0.0, 0.0, axis_eps)] * 3, dtype=wp.vec3, device=device)
        self.axes_ends = wp.array([
            wp.vec3(axis_length, 0.0, axis_eps),
            wp.vec3(0.0, axis_length, axis_eps),
            wp.vec3(0.0, 0.0, axis_length + axis_eps)
        ], dtype=wp.vec3, device=device)
        self.axes_colors = wp.array([
            wp.vec3(1.0, 0.0, 0.0), wp.vec3(0.0, 1.0, 0.0), wp.vec3(0.0, 0.0, 1.0)
        ], dtype=wp.vec3, device=device)

        self.time = 0.0
        self.spacing = 2.0
        self.renderer = getattr(self.viewer, "renderer", None)

    def gui(self, ui):
        ui.text("Simulation Controls")
        if ui.button("Reset Simulation"):
            self.time = 0.0
            # If you had physics state, you would reset it here
            print("Simulation Reset!")
            
        ui.separator()
        ui.text("Custom UI text")
        _changed, self.time = ui.slider_float("Time", self.time, 0.0, 100.0)
        _changed, self.spacing = ui.slider_float("Spacing", self.spacing, 0.0, 10.0)

    def step(self):
        pass

    def render(self):
        self.viewer.begin_frame(self.time)

        base_height, base_left = 2.0, -4.0
        qy = wp.quat_from_axis_angle(wp.vec3(0, 1, 0), 0.3 * self.time)
        qx = wp.quat_from_axis_angle(wp.vec3(1, 0, 0), 0.2 * self.time)
        qz = wp.quat_from_axis_angle(wp.vec3(0, 0, 1), 0.4 * self.time)

        # Helper to create single-element transform arrays on the correct device
        def make_xform(pos, rot):
            return wp.array([wp.transform(pos, rot)], dtype=wp.transform, device=device)

        # Log Primitives
        self.viewer.log_shapes("/sphere", newton.GeoType.SPHERE, 0.5, make_xform([0, base_left, base_height + 0.3 * abs(math.sin(self.time))], qy), self.col_sphere, self.mat_default)
        base_left += self.spacing
        
        self.viewer.log_shapes("/box", newton.GeoType.BOX, (0.5, 0.3, 0.8), make_xform([0, base_left, base_height], qx), self.col_box, self.mat_default)
        base_left += self.spacing

        self.viewer.log_shapes("/cone", newton.GeoType.CONE, (0.4, 1.2), make_xform([0, base_left, base_height], qy), self.col_cone, self.mat_default)
        base_left += self.spacing

        # Log Bunny only if it loaded safely
        if self.bunny_mesh:
            self.viewer.log_shapes("/bunny", newton.GeoType.MESH, (1, 1, 1), make_xform([0, base_left + 2.0, base_height], qz), self.col_bunny, self.mat_default, geo_src=self.bunny_mesh)

        # Plane
        self.viewer.log_shapes("/plane", newton.GeoType.PLANE, (50.0, 50.0), wp.array([wp.transform_identity()], dtype=wp.transform, device=device), self.col_plane, self.mat_plane)

        self.viewer.log_lines("/axes", self.axes_begins, self.axes_ends, self.axes_colors)
        self.viewer.end_frame()
        self.time += 1.0 / 60.0

if __name__ == "__main__":
    import time
    # Parse arguments and initialize viewer
    viewer, args = newton.examples.init()
    
    # Give the GL context a moment to breathe
    time.sleep(0.5)

    example = Example(viewer, args)
    newton.examples.run(example, args)