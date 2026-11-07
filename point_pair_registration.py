import open3d as o3d
from pathlib import Path

gt_path = Path(
    r"C:\Users\gwx1492938\Desktop\mini-colmap-viewer\data\small\scan1_small.ply"
)

pred_path = Path(
    r"C:\Users\gwx1492938\Desktop\mini-colmap-viewer\data\synthetic\pred_rotate.ply"
)

gt = o3d.io.read_point_cloud(
    str(gt_path)
)

pred = o3d.io.read_point_cloud(
    str(pred_path)
)

print("GT loaded!")
print(f"GT points: {len(gt.points):,}")

print("Pred loaded!")
print(f"Pred points: {len(pred.points):,}")

gt_idx = [
    98052,
    26715,
    6936
]

pred_idx = [
    297575,
    73687,
    321261
]

print()
print("GT point 1:")
print(gt.points[gt_idx[0]])

print()
print("Pred point 1:")
print(pred.points[pred_idx[0]])

import numpy as np

gt_points = np.array([
    gt.points[gt_idx[0]],
    gt.points[gt_idx[1]],
    gt.points[gt_idx[2]]
])

pred_points = np.array([
    pred.points[pred_idx[0]],
    pred.points[pred_idx[1]],
    pred.points[pred_idx[2]]
])

print()
print("GT control points:")
print(gt_points)

print()
print("Pred control points:")
print(pred_points)

# =========================
# Create control-point clouds
# =========================

gt_control = o3d.geometry.PointCloud()

gt_control.points = o3d.utility.Vector3dVector(
    gt_points
)

pred_control = o3d.geometry.PointCloud()

pred_control.points = o3d.utility.Vector3dVector(
    pred_points
)

# =========================
# Define correspondences
# =========================

correspondences = o3d.utility.Vector2iVector([
    [0, 0],
    [1, 1],
    [2, 2]
])

print()
print("Correspondences created!")

# =========================
# Estimate transformation
# =========================

estimator = (
    o3d.pipelines.registration
    .TransformationEstimationPointToPoint()
)

transformation = estimator.compute_transformation(
    pred_control,
    gt_control,
    correspondences
)

print()
print("===== Initial Transform =====")
print(transformation)