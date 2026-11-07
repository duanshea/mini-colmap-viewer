import copy
import numpy as np
import open3d as o3d
from pathlib import Path

#输入输出路径
input_path =Path(r"C:\Users\gwx1492938\Desktop\mini-colmap-viewer\data\small\scan1_small.ply")

output_dir = Path(
    r"C:\Users\gwx1492938\Desktop\mini-colmap-viewer\data\synthetic"
)

#读取GT
print("Loading GT point cloud...")

gt = o3d.io.read_point_cloud(
    str(input_path)
)

print(f"Points: {len(gt.points):,}")

#保存函数
def save_cloud(
        pcd,
        filename
):
    output_path = output_dir / filename

    o3d.io.write_point_cloud(
        str(output_path),
        pcd
    )
    print(f"Saved: {filename}")

save_cloud(
    gt,
    "test.ply"
)

# Case 1: translation Only
pcd_translate = copy.deepcopy(gt)

pcd_translate.translate(
    [0.1,0,0]
)

save_cloud(
    pcd_translate,
    "pred_translate.ply"
)

# Case 2: Rotation Only
pcd_rotate = copy.deepcopy(gt)
R = pcd_rotate.get_rotation_matrix_from_xyz(
    (
        0,
        0,
        np.deg2rad(10)
    )
)

pcd_rotate.rotate(
    R,
    center=pcd_rotate.get_center()
)

pcd_rotate.rotate(
    R,
    center=pcd_rotate.get_center()
)

save_cloud(
    pcd_rotate,
    "pred_rotate.ply"
)