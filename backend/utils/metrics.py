import open3d as o3d
from pathlib import Path
import math

# =========================
# Configuration
# =========================
PRED_FILE = "pred_aligned.ply"

# =========================
# Paths
# =========================

gt_path = Path(
    r"C:\Users\gwx1492938\Desktop\mini-colmap-viewer\data\small\scan1_small.ply"
)

pred_path = Path(
    rf"C:\Users\gwx1492938\Desktop\mini-colmap-viewer\data\synthetic\{PRED_FILE}"
)

# =========================
# Load point clouds
# =========================

gt = o3d.io.read_point_cloud(str(gt_path))
pred = o3d.io.read_point_cloud(str(pred_path))

print(f"GT points: {len(gt.points):,}")
print(f"Pred points: {len(pred.points):,}")

# =========================
# Build KDTree
# =========================

pred_tree = o3d.geometry.KDTreeFlann(pred)

print("KDTree created!")

# =========================
# Compute C2C distances
# =========================

distances = []

for point in gt.points:

    k, idx, dist = pred_tree.search_knn_vector_3d(
        point,
        1
    )

    distance = math.sqrt(dist[0])

    distances.append(distance)

print(f"Distances computed: {len(distances):,}")

print("First 5 distances:")
print(distances[:5])

# =========================
# Statistics
# =========================

mean_distance = sum(distances) / len(distances)

rmse = math.sqrt(
    sum(d * d for d in distances)
    / len(distances)
)

min_distance = min(distances)

max_distance = max(distances)

print()
print("===== C2C Statistics =====")

print(f"Mean Distance : {mean_distance:.6f} m")
print(f"RMSE          : {rmse:.6f} m")
print(f"Min Distance  : {min_distance:.6f} m")
print(f"Max Distance  : {max_distance:.6f} m")