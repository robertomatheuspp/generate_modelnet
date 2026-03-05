import open3d as o3d
import trimesh
import numpy as np
import os
from PIL import Image



# -------- SETTINGS --------
MODELNET_ROOT = r"./ModelNet10"
"""
My structure is
./ 
    ./ModenNet10 
        ./bathtub
            ./test
            ./train
                bathtub_0001.off
                bathtub_0002.off
                ...
        ...
        ./bookshelf
    ./ModelNet10_views
    ./modelnet40_2Dgen.py
"""


OUTPUT_ROOT = r"./ModelNet10_views"
NUM_VIEWS = 12
IMAGE_SIZE = 224
CAM_DISTANCE = 2.5
ELEVATION = 30
# --------------------------


import numpy as np

def rotation_matrix_4x4(rx=0, ry=0, rz=0):
    """Return a 4x4 homogeneous rotation matrix from xyz rotations in radians"""
    R3 = o3d.geometry.TriangleMesh.get_rotation_matrix_from_xyz((rx, ry, rz))
    R4 = np.eye(4)
    R4[:3, :3] = R3
    return R4
    
def render_mesh_offscreen(mesh_path, output_dir):
    # Load and normalize mesh
    mesh_tm = trimesh.load(mesh_path)
    mesh_tm.vertices -= mesh_tm.vertices.mean(axis=0)
    mesh_tm.vertices /= np.max(np.abs(mesh_tm.vertices))

    mesh = o3d.geometry.TriangleMesh(
        o3d.utility.Vector3dVector(mesh_tm.vertices),
        o3d.utility.Vector3iVector(mesh_tm.faces)
    )
    mesh.compute_vertex_normals()

    # Offscreen renderer
    renderer = o3d.visualization.rendering.OffscreenRenderer(IMAGE_SIZE, IMAGE_SIZE)
    mat = o3d.visualization.rendering.MaterialRecord()
    mat.shader = "defaultLit"
    renderer.scene.add_geometry("mesh", mesh, mat)

    center = mesh.get_center()
    for i in range(NUM_VIEWS):
        angle = 360 * i / NUM_VIEWS
        R4 = rotation_matrix_4x4(0, 0, np.radians(angle))
        renderer.scene.set_geometry_transform("mesh", R4)

        # Camera
        renderer.setup_camera(
            vertical_field_of_view=60.0,
            center=center,
            eye=[CAM_DISTANCE, 0, 0],
            up=[0, 0, 1]
        )

        img = renderer.render_to_image()
        img_pil = Image.fromarray(np.asarray(img))
        img_path = os.path.join(output_dir, f"{i:03d}.png")
        img_pil.save(img_path)

    # renderer.release_renderer()


# Example usage (first 10 meshes)
count = 0
for category in os.listdir(MODELNET_ROOT):
    category_path = os.path.join(MODELNET_ROOT, category)
    if not os.path.isdir(category_path):
        continue

    for split in ["train", "test"]:
        split_path = os.path.join(category_path, split)
        if not os.path.exists(split_path):
            continue

        for model_file in os.listdir(split_path):
            if not model_file.endswith(".off"):
                continue

            model_path = os.path.join(split_path, model_file)
            obj_name = model_file.replace(".off", "")
            out_dir = os.path.join(OUTPUT_ROOT, category, split, obj_name)
            os.makedirs(out_dir, exist_ok=True)

            print(f"Rendering {model_path}")
            render_mesh_offscreen(model_path, out_dir)

            count += 1
    if count == 2:
        break
