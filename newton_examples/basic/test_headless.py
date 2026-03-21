import warp as wp
import numpy as np
import newton

wp.init()
try:
    print("Attempting to initialize Newton Engine...")
    v = np.array([[0,0,0], [1,0,0], [0,1,0]], dtype=np.float32)
    f = np.array([0,1,2], dtype=np.int32)
    m = newton.Mesh(v, f)
    m.finalize()
    print("SUCCESS: Newton Engine is healthy on your GPU!")
except Exception as e:
    print(f"FAILED: {e}")