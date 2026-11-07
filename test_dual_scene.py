
from pathlib import Path
import open3d as o3d
import open3d.visualization.gui as gui
import open3d.visualization.rendering as rendering

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

print(
    f"GT points: {len(gt.points):,}"
)

print(
    f"Pred points: {len(pred.points):,}"
)

gui.Application.instance.initialize()

window = gui.Application.instance.create_window(
    "Dual Scene Test",
    1200,
    700
)

layout = gui.Horiz()

window.add_child(layout)

scene_left = gui.SceneWidget()
scene_right = gui.SceneWidget()

print("left scene created")
print("right scene created")


scene_left.scene = rendering.Open3DScene(
    window.renderer
)

scene_right.scene = rendering.Open3DScene(
    window.renderer
)

scene_left.scene.set_background([1, 0, 0, 1])
scene_right.scene.set_background([0, 0, 1, 1])

layout.add_child(scene_left)
layout.add_child(scene_right)

axis_left = o3d.geometry.TriangleMesh.create_coordinate_frame()
axis_right = o3d.geometry.TriangleMesh.create_coordinate_frame()

material = rendering.MaterialRecord()
material.shader = "defaultLit"
material.point_size = 3.0

scene_left.scene.add_geometry(
    "gt",
    axis_left,
    material
)

scene_right.scene.add_geometry(
    "pred",
    axis_right,
    material
)

bbox = axis_left.get_axis_aligned_bounding_box()

bbox_left = gt.get_axis_aligned_bounding_box()

bbox_right = pred.get_axis_aligned_bounding_box()


scene_left.setup_camera(
    60,
    bbox,
    bbox.get_center()
)

scene_right.setup_camera(
    60,
    bbox,
    bbox.get_center()
)

def on_layout(layout_context):

    content_rect = window.content_rect

    layout.frame = content_rect

window.set_on_layout(
    on_layout
)

gui.Application.instance.run()