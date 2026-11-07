import open3d as o3d
import time
from pathlib import Path

"""
Generate development-scale point cloud.

ETH3D scan1:
24,253,058 points
↓ voxel_size=0.02 m
376,743 points
"""

ply_path = Path(
    r"C:\Users\gwx1492938\Desktop\mini-colmap-viewer\data\raw\scan1.ply"
)

start = time.time()

pcd = o3d.io.read_point_cloud(str(ply_path))

end = time.time()
print(f"Loading time: {end-start:.2f} seconds")
print(f"Number of points: {len(pcd.points):,}")

print("Downsampling...")

pcd_small = pcd.voxel_down_sample(
    voxel_size=0.02
)

print(f"Downsampled points: {len(pcd_small.points):,}")

output_path = Path(
    r"C:\Users\gwx1492938\Desktop\mini-colmap-viewer\data\small\scan1_small.ply"
)

o3d.io.write_point_cloud(
    str(output_path),
    pcd_small
)

print("Saved!")