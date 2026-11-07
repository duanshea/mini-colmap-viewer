import open3d as o3d
from pathlib import Path

gt_path = Path(
    r"C:\Users\gwx1492938\Desktop\mini-colmap-viewer\data\small\scan1_small.ply"
)

pred_path = Path(
    r"C:\Users\gwx1492938\Desktop\mini-colmap-viewer\data\synthetic\pred_rotate.ply"
)

gt = o3d.io.read_point_cloud(str(gt_path))
pred = o3d.io.read_point_cloud(str(pred_path))

print(f"GT points: {len(gt.points):,}")
print(f"Pred points: {len(pred.points):,}")

# 给icp一个初始变换
import numpy as np
initial_transform = np.eye(4)
print(initial_transform)

result = o3d.pipelines.registration.registration_icp(
    pred,
    gt,
    0.2,
    initial_transform
)

print(result)
print("Transformation matrix:")
print(result.transformation)
print(f"Fitness: {result.fitness:.6f}")
print(f"RMSE: {result.inlier_rmse:.6f}")