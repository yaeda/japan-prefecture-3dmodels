import os
import sys

import numpy as np
import trimesh


def lift_non_bottom_vertices(mesh, thickness=1.0, threshold=1e-4):
    vertices = mesh.vertices.copy()
    y_min = np.min(vertices[:, 1])

    # Y=最小値以外の頂点を上にずらす
    mask = np.abs(vertices[:, 1] - y_min) > threshold
    vertices[mask, 1] += thickness

    return trimesh.Trimesh(vertices=vertices, faces=mesh.faces.copy())

def process_lift_thickness(input_path, output_path=None, thickness=1.0):
    mesh = trimesh.load_mesh(input_path, process=True)

    print(f"⬆️ Y={np.min(mesh.vertices[:, 1])} より高い頂点を {thickness} 上に持ち上げ中...")
    modified_mesh = lift_non_bottom_vertices(mesh, thickness=thickness)

    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = base + "_+${thickness}mm.stl"

    modified_mesh.export(output_path)
    print(f"✅ 厚みを追加したSTLを保存しました: {output_path}")

# CLI
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python thicken.py input.stl [output.stl] [thickness(mm)]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    thickness = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0

    process_lift_thickness(input_path, output_path, thickness)
