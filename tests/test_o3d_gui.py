
import open3d as o3d
import open3d.visualization.gui as gui
import open3d.visualization.rendering as rendering
from pathlib import Path

gui.Application.instance.initialize()

window = gui.Application.instance.create_window(
    "Open3D GUI Test",
    1000,
    700
)

scene_widget = gui.SceneWidget()
window.add_child(
    scene_widget
)

scene = rendering.Open3DScene(
    window.renderer
)

axis = o3d.geometry.TriangleMesh.create_coordinate_frame()
pcd_path = Path(
    r"C:\Users\gwx1492938\Desktop\mini-colmap-viewer\data\small\scan1_small.ply"
)

pcd = o3d.io.read_point_cloud(
    str(pcd_path)
)

print(
    f"Loaded points: {len(pcd.points):,}"
)

scene_widget.scene = scene

material = rendering.MaterialRecord()
material.shader = "defaultUnlit"

scene.add_geometry(
    "axis",
    axis,
    material
)

scene.add_geometry(
    "pointcloud",
    pcd,
    material
)

print("Axis added")
bbox = axis.get_axis_aligned_bounding_box()
scene_widget.setup_camera(
    60,
    bbox,
    bbox.get_center()
)
print(pcd.get_center())
gui.Application.instance.run()