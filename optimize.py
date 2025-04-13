import argparse

import numpy as np
import trimesh
from scipy.spatial import ConvexHull
from shapely.geometry import LineString, Point, Polygon


# Lift all vertices that are not at the bottom Y to add thickness
def lift_non_bottom_vertices(mesh, thickness=1.0, threshold=1e-4):
    vertices = mesh.vertices.copy()
    y_min = np.min(vertices[:, 1])
    mask = np.abs(vertices[:, 1] - y_min) > threshold
    vertices[mask, 1] += thickness
    return trimesh.Trimesh(vertices=vertices, faces=mesh.faces.copy())

# Move bottom vertices that lie outside the terrain boundary polygon
def adjust_outside_bottom_vertices(mesh, threshold=1e-4):
    vertices = mesh.vertices.copy()
    y_min = np.min(vertices[:, 1])

    # Create a 2D convex hull from topography (Y > min) to get the terrain boundary
    top_vertices = vertices[vertices[:, 1] > y_min + threshold]
    if len(top_vertices) < 3:
        print("⚠️ Not enough top vertices for convex hull.")
        return mesh

    projected_top = top_vertices[:, [0, 2]]
    try:
        hull = ConvexHull(projected_top)
        hull_coords = projected_top[hull.vertices]
        polygon = Polygon(hull_coords)
    except:
        print("⚠️ Failed to generate terrain boundary polygon.")
        return mesh

    # Check bottom vertices (Y ≈ min) and project to XZ
    mask_bottom = np.abs(vertices[:, 1] - y_min) < threshold
    bottom_indices = np.where(mask_bottom)[0]
    bottom_vertices = vertices[bottom_indices]
    projected_bottom = bottom_vertices[:, [0, 2]]
    center = np.mean(projected_top, axis=0)

    updated_vertices = vertices.copy()
    move_count = 0

    for idx, pt in zip(bottom_indices, projected_bottom):
        point = Point(pt)
        if polygon.contains(point):
            continue

        # Move point to intersection between polygon boundary and line to center
        ray = LineString([tuple(center), tuple(pt)])
        intersection = polygon.exterior.intersection(ray)

        new_pt = None
        if intersection.is_empty:
            continue
        elif intersection.geom_type == "MultiPoint":
            points = list(intersection.geoms)
            closest = min(points, key=lambda p: np.linalg.norm(np.array(p.coords[0]) - center))
            new_pt = np.array(closest.coords[0])
        elif intersection.geom_type == "Point":
            new_pt = np.array(intersection.coords[0])
        else:
            continue

        updated_vertices[idx, 0] = new_pt[0]
        updated_vertices[idx, 2] = new_pt[1]
        move_count += 1

    print(f"🧭 Moved {move_count} bottom vertices into the terrain boundary.")
    return trimesh.Trimesh(vertices=updated_vertices, faces=mesh.faces.copy())

# Main processing logic: lift model and optionally adjust bottom boundary
def process_model(input_file, output_file, thickness=1.0, skip_adjustment=False):
    mesh = trimesh.load_mesh(input_file, process=True)
    print(f"⬆️ 底面以外の頂点を {thickness}mm 持ち上げています...")
    lifted = lift_non_bottom_vertices(mesh, thickness)

    if not skip_adjustment:
        print("📐 地形ポリゴン外の底面頂点を調整しています...")
        lifted = adjust_outside_bottom_vertices(lifted)

    lifted.export(output_file)
    print(f"✅ 出力完了: {output_file}")

# CLI interface
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Optimize 3D terrain models for printing (thickness + bottom adjustment)")
    parser.add_argument("input_file", help="Input STL file")
    parser.add_argument("output_file", help="Output STL file")
    parser.add_argument("thickness", type=float, default=1.0, help="厚み（mm）: 非底面の頂点を持ち上げる量（デフォルト: 1.0mm）")
    parser.add_argument("--skip-adjustment", action="store_true", help="底面形状の調整をスキップする")

    args = parser.parse_args()
    process_model(args.input_file, args.output_file, args.thickness, args.skip_adjustment)
