import open3d as o3d
from pathlib import Path

gt_path = Path(
    r"C:\Users\gwx1492938\Desktop\mini-colmap-viewer\data\synthetic\pred_rotate.ply"
)

pcd = o3d.io.read_point_cloud(
    str(gt_path)
)
print("Loaded!")
print(f"Points: {len(pcd.points):,}")

print("")
print("Instructions:")
print("Shift + Left Click = Pick Point")
print("Shift + Right Click = Undo")
print("Press Q = Finish")
print("")

vis = o3d.visualization.VisualizerWithEditing()

vis.create_window()

vis.add_geometry(pcd)

vis.run()

vis.destroy_window()

picked = vis.get_picked_points()

print("")
print("Picked point indices:")
print(picked)