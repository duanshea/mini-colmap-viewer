import open3d as o3d
from pathlib import Path

gt_path = Path(
    r"C:\Users\gwx1492938\Desktop\mini-colmap-viewer\data\small\scan1_small.ply"
)

pred_path = Path(
    r"C:\Users\gwx1492938\Desktop\mini-colmap-viewer\data\synthetic\pred_translate.ply"
)

gt = o3d.io.read_point_cloud(str(gt_path))
pred = o3d.io.read_point_cloud(str(pred_path))

print("GT center:")
print(gt.get_center())

print("Pred center:")
print(pred.get_center())



translation = (
    gt.get_center()
    -
    pred.get_center()
)

print("Translation vector:")
print(translation)

pred.translate(translation)
print("Pred center after alignment:")
print(pred.get_center())

aligned_path = Path(
    r"C:\Users\gwx1492938\Desktop\mini-colmap-viewer\data\synthetic\pred_aligned.ply"
)

o3d.io.write_point_cloud(
    str(aligned_path),
    pred
)

print("Aligned point cloud saved!")