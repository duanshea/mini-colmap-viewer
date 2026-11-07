import copy
from pathlib import Path

import open3d as o3d

# 输入点云
input_path = Path(
    r"C:\Users\gwx1492938\Desktop\mini-colmap-viewer\data\small\scan1_small.ply"
)

# 输出点云
output_path = Path(
    r"C:\Users\gwx1492938\Desktop\mini-colmap-viewer\data\synthetic\pred_translate.ply"
)

print("Loading point cloud...")

pcd = o3d.io.read_point_cloud(str(input_path))

print(f"Points: {len(pcd.points):,}")

# 深拷贝，保护原始GT
pcd_pred = copy.deepcopy(pcd)

print("Applying translation...")

# X方向平移10cm
pcd_pred.translate([0.1, 0, 0])

print("Saving point cloud...")

o3d.io.write_point_cloud(
    str(output_path),
    pcd_pred
)

print("Done!")
print(f"Saved to: {output_path}")