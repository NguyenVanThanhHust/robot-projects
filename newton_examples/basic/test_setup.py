import warp as wp
import newton
import newton.examples

wp.init()
# If this crashes, the issue is the UI/Renderer initialization
viewer, args = newton.examples.init()
print("Viewer initialized successfully")