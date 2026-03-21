import warp as wp
wp.init()

@wp.kernel
def test(x: wp.array(dtype=float)):
    tid = wp.tid()  # This was the missing line!
    x[tid] = x[tid] * 2.0

# Explicitly use cuda:0
device = "cuda:0"
data = wp.array([1.0, 2.0, 3.0], dtype=float, device=device)

wp.launch(test, dim=3, inputs=[data], device=device)
wp.synchronize()

print(f"Warp Compute Success: {data.numpy()}")