import open3d as o3d
from pathlib import Path

gt_path = Path(
    r"C:\Users\gwx1492938\Desktop\mini-colmap-viewer\data\small\scan1_small.ply"
)

gt = o3d.io.read_point_cloud(str(gt_path))

o3d.visualization.draw_geometries([gt])