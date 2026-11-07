
from pathlib import Path
import numpy as np
import open3d as o3d
import open3d.visualization.gui as gui
import open3d.visualization.rendering as rendering





# =========================
# Load Point Clouds
# =========================
selected_gt_points = []

selected_pred_points = []
pick_history = []

#current_transform = np.eye(4)
current_transform = np.array([
    [ 9.39631531e-01,  3.42187685e-01,  4.17906839e-04, -2.29169249e-02],
    [-3.42187490e-01,  9.39627615e-01,  2.76892246e-03,  1.94412570e-01],
    [ 5.54814359e-04, -2.74476934e-03,  9.99996079e-01,  7.90927189e-03],
    [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]
])

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


# =========================
# Bounding Box
# =========================

bbox_left = gt.get_axis_aligned_bounding_box()

bbox_right = pred.get_axis_aligned_bounding_box()

center_left = bbox_left.get_center()

center_right = bbox_right.get_center()

print()
print("GT bbox center:")
print(center_left)

print()
print("Pred bbox center:")
print(center_right)


# =========================
# Coordinate Axes
# =========================

axis_gt = o3d.geometry.TriangleMesh.create_coordinate_frame(
    size=0.5
)

axis_gt.translate(
    center_left
)

axis_pred = o3d.geometry.TriangleMesh.create_coordinate_frame(
    size=0.5
)

axis_pred.translate(
    center_right
)


# =========================
# Open3D GUI
# =========================

gui.Application.instance.initialize()

window = gui.Application.instance.create_window(
    "Dual Scene V2",
    1400,
    800
)


# =========================
# Left Scene
# =========================

scene_left = gui.SceneWidget()

scene_left.scene = rendering.Open3DScene(
    window.renderer
)


# =========================
# Right Scene
# =========================

scene_right = gui.SceneWidget()

scene_right.scene = rendering.Open3DScene(
    window.renderer
)


window.add_child(
    scene_left
)

window.add_child(
    scene_right
)

panel = gui.Vert()

window.add_child(
    panel
)

pair_label = gui.Label(
    "Matched Points"
)

panel.add_child(
    pair_label
)

pair_list = gui.ListView()

panel.add_child(
    pair_list
)



estimate_button = gui.Button(
    "Registration"
)

icp_button = gui.Button(
    "Run ICP"
)

undo_button = gui.Button(
    "Undo Last"
)

panel.add_child(
    undo_button
)


panel.add_child(
    icp_button
)

panel.add_child(
    estimate_button
)


# =========================
# Material
# =========================

material = rendering.MaterialRecord()

material.shader = "defaultUnlit"

material.point_size = 3.0


# =========================
# Add Geometry
# =========================

scene_left.scene.add_geometry(
    "gt",
    gt,
    material
)

scene_left.scene.add_geometry(
    "gt_axis",
    axis_gt,
    material
)

scene_right.scene.add_geometry(
    "pred",
    pred,
    material
)

scene_right.scene.add_geometry(
    "pred_axis",
    axis_pred,
    material
)


# =========================
# Camera
# =========================

scene_left.setup_camera(
    60,
    bbox_left,
    bbox_left.get_center()
)



scene_right.setup_camera(
    60,
    bbox_right,
    bbox_right.get_center()
)


# =========================
# Layout
# =========================

def on_key(event):

    if (
        event.type ==
        gui.KeyEvent.DOWN
        and
        event.key == gui.KeyName.Z
        and
        event.is_modifier_down(
            gui.KeyModifier.CTRL
        )
    ):

        on_undo()
        return gui.Widget.EventCallbackResult.HANDLED

    return gui.Widget.EventCallbackResult.IGNORED

def on_layout(layout_context):

    rect = window.content_rect

    panel_height = 400

    width = rect.width // 2

    scene_height = rect.height - panel_height

    scene_left.frame = gui.Rect(
        rect.x,
        rect.y,
        width,
        scene_height
    )

    scene_right.frame = gui.Rect(
        rect.x + width,
        rect.y,
        width,
        scene_height

    )

    panel.frame = gui.Rect(
        rect.x,
        rect.y + scene_height,
        rect.width,
        panel_height
    )


window.set_on_layout(
    on_layout
)

def on_left_mouse(event):

    if event.type != gui.MouseEvent.Type.BUTTON_DOWN:
        return gui.Widget.EventCallbackResult.IGNORED

    if not event.is_modifier_down(
        gui.KeyModifier.SHIFT
    ):
        return gui.Widget.EventCallbackResult.IGNORED

    print("SHIFT PICK")

    mouse_x = int(
        event.x - scene_left.frame.x
    )

    mouse_y = int(
        event.y - scene_left.frame.y
    )

    def depth_callback(depth_image):

        depth = np.asarray(
            depth_image
        )

        d = depth[
            mouse_y,
            mouse_x
        ]

        if d >= 0.9999:

            print(
                "Background clicked"
            )

            return

        print(
            f"Mouse: ({mouse_x}, {mouse_y})"
        )

        print(
            f"Depth: {d}"
        )

        world = scene_left.scene.camera.unproject(
            mouse_x,
            mouse_y,
            d,
            depth.shape[1],
            depth.shape[0]
        )

        print(
            "World:"
        )

        print(
            world
        )

        selected_gt_points.append(
            world.tolist()
        )

        pick_history.append(
            ("gt", len(selected_gt_points))
        )

        print(
            pick_history
        )

        sphere = o3d.geometry.TriangleMesh.create_sphere(
            radius=0.05
        )

        sphere.paint_uniform_color(
            [1, 0, 0]
        )

        sphere.translate(
            world
        )

        scene_left.scene.add_geometry(
            f"gt_pick_{len(selected_gt_points)}",
            sphere,
            material
        )

        print(
            f"GT Points: {len(selected_gt_points)}"
        )

        pair_items = []

        for i in range(
            len(selected_gt_points)
        ):

            pair_items.append(
                f"GT #{i + 1}"
            )

        pair_list.set_items(
            pair_items
        )

    scene_left.scene.scene.render_to_depth_image(
        depth_callback
    )

    return gui.Widget.EventCallbackResult.HANDLED


def on_right_mouse(event):

    if event.type != gui.MouseEvent.Type.BUTTON_DOWN:
        return gui.Widget.EventCallbackResult.IGNORED

    if not event.is_modifier_down(
        gui.KeyModifier.SHIFT
    ):
        return gui.Widget.EventCallbackResult.IGNORED

    print("SHIFT PICK")

    mouse_x = int(
        event.x - scene_right.frame.x
    )

    mouse_y = int(
        event.y - scene_right.frame.y
    )

    def depth_callback(depth_image):

        depth = np.asarray(
            depth_image
        )

        d = depth[
            mouse_y,
            mouse_x
        ]

        if d >= 0.9999:

            print(
                "Background clicked"
            )

            return

        print(
            f"Mouse: ({mouse_x}, {mouse_y})"
        )

        print(
            f"Depth: {d}"
        )

        world = scene_right.scene.camera.unproject(
            mouse_x,
            mouse_y,
            d,
            depth.shape[1],
            depth.shape[0]
        )

        print(
            "World:"
        )

        print(
            world
        )

        selected_pred_points.append(
            world.tolist()
        )

        pick_history.append(
            ("pred", len(selected_pred_points))
        )

        print(
            pick_history
        )


        sphere = o3d.geometry.TriangleMesh.create_sphere(
            radius=0.05
        )

        sphere.paint_uniform_color(
            [0, 1, 0]
        )

        sphere.translate(
            world
        )

        scene_right.scene.add_geometry(
            f"pred_pick_{len(selected_pred_points)}",
            sphere,
            material
        )

        print(
            f"Pred Points: {len(selected_pred_points)}"
        )

        pair_items = []

        for i in range(
            len(selected_pred_points)
        ):

            pair_items.append(
                f"Pred #{i + 1}"
            )

        pair_list.set_items(
            pair_items
        )

    scene_right.scene.scene.render_to_depth_image(
        depth_callback
    )

    return gui.Widget.EventCallbackResult.HANDLED

def on_estimate_transform():

    print()
    print("===== Estimate Transform =====")

    gt_pts = np.asarray(
        selected_gt_points,
        dtype=np.float64
    )

    pred_pts = np.asarray(
        selected_pred_points,
        dtype=np.float64
    )

    print(
        f"GT shape: {gt_pts.shape}"
    )

    print(
        f"Pred shape: {pred_pts.shape}"
    )

    if len(gt_pts) != len(pred_pts):

        print(
            "Point count mismatch!"
        )

        return

    if len(gt_pts) < 3:

        print(
            "Need at least 3 pairs!"
        )

        return

    source = o3d.geometry.PointCloud()

    source.points = (
        o3d.utility.Vector3dVector(
            pred_pts
        )
    )

    target = o3d.geometry.PointCloud()

    target.points = (
        o3d.utility.Vector3dVector(
            gt_pts
        )
    )

    corr = np.column_stack([
        np.arange(len(gt_pts)),
        np.arange(len(gt_pts))
    ])

    corr = o3d.utility.Vector2iVector(
        corr
    )

    T = (
        o3d.pipelines.registration.
        TransformationEstimationPointToPoint()
    ).compute_transformation(
        source,
        target,
        corr
    )

    global current_transform

    current_transform = T

    print()
    print("Transformation:")

    print(T)
    print()

    pred_copy = o3d.geometry.PointCloud(
        pred
    )

    pred_copy.transform(
        T
    )

    scene_right.scene.remove_geometry(
        "pred"
    )

    scene_right.scene.add_geometry(
        "pred",
        pred_copy,
        material
    )

    print(
        "GT center:"
    )

    print(
        gt.get_axis_aligned_bounding_box().get_center()
    )

    print()

    print(
        "Pred transformed center:"
    )

    print(
        pred_copy.get_axis_aligned_bounding_box().get_center()
    )

    scene_right.scene.remove_geometry(
        "pred"
    )

    scene_right.scene.add_geometry(
        "pred",
        pred_copy,
        material
    )


def on_undo():

    if len(pick_history) == 0:

        print(
            "Nothing to undo"
        )

        return

    point_type, point_id = pick_history.pop()

    if point_type == "gt":

        selected_gt_points.pop()

        scene_left.scene.remove_geometry(
            f"gt_pick_{point_id}"
        )

        print(
            f"Undo GT #{point_id}"
        )

    else:

        selected_pred_points.pop()

        scene_right.scene.remove_geometry(
            f"pred_pick_{point_id}"
        )

        print(
            f"Undo Pred #{point_id}"
        )

def on_run_icp():

    global current_transform

    print()
    print("===== ICP =====")

    result = (
        o3d.pipelines.registration.registration_icp(
            pred,
            gt,
            0.5,
            current_transform,
            o3d.pipelines.registration.
            TransformationEstimationPointToPoint()
        )
    )

    print()

    print(
        "Fitness:"
    )

    print(
        result.fitness
    )

    print()

    print(
        "RMSE:"
    )

    print(
        result.inlier_rmse
    )

    print()

    print(
        "ICP Transform:"
    )

    print(
        result.transformation
    )

    pred_icp = o3d.geometry.PointCloud(
        pred
    )

    pred_icp.transform(
        result.transformation
    )

    scene_right.scene.remove_geometry(
        "pred"
    )

    scene_right.scene.add_geometry(
        "pred",
        pred_icp,
        material
    )


scene_left.set_on_mouse(
    on_left_mouse
)

scene_right.set_on_mouse(
    on_right_mouse
)




estimate_button.set_on_clicked(
    on_estimate_transform
)

undo_button.set_on_clicked(
    on_undo
)

icp_button.set_on_clicked(
    on_run_icp
)

window.set_on_key(
    on_key
)

# =========================
# Run
# =========================

gui.Application.instance.run()