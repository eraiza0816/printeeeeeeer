import numpy as np
from stl import mesh

# Parameters
outer_radius = 9.7 / 2  # mm
inner_radius = 7.8 / 2  # mm
tube_height = 3.5  # mm (Tube thickness)
base_radius = 12 / 2  # mm
base_height = 1.0  # mm (Base thickness)
segments = 100  # Smoothness of the circular shape

# Function to create a cylinder mesh
def create_cylinder(radius, height, segments, z_offset=0):
    theta = np.linspace(0, 2 * np.pi, segments, endpoint=False)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    z_bottom = np.zeros_like(x) + z_offset
    z_top = np.full_like(x, height) + z_offset
    vertices_bottom = np.column_stack((x, y, z_bottom))
    vertices_top = np.column_stack((x, y, z_top))
    return vertices_bottom, vertices_top

# Generate vertices for the solid base (at z=0)
base_bottom, base_top = create_cylinder(base_radius, base_height, segments)

# Generate vertices for the main tube (positioned on top of the base)
outer_bottom, outer_top = create_cylinder(outer_radius, tube_height, segments, z_offset=base_height)
inner_bottom, inner_top = create_cylinder(inner_radius, tube_height - 0.5, segments, z_offset=base_height + 0.5)

# Combine all vertices
vertices = np.vstack((base_bottom, base_top, outer_bottom, outer_top, inner_bottom, inner_top))

# Create faces
faces = []

# Create faces for the solid base
for i in range(segments):
    next_idx = (i + 1) % segments
    # Side walls of the base
    faces.append([i, next_idx, segments + i])
    faces.append([next_idx, segments + next_idx, segments + i])
    # Top face of the base
    faces.append([segments + i, segments + next_idx, segments + i])

# Offset for the tube vertices
offset_outer = 2 * segments

# Create outer wall faces for the main tube
for i in range(segments):
    next_idx = (i + 1) % segments
    faces.append([offset_outer + i, offset_outer + next_idx, offset_outer + segments + i])  # Bottom to top
    faces.append([offset_outer + next_idx, offset_outer + segments + next_idx, offset_outer + segments + i])

# Create inner wall faces for the main tube
offset_inner = offset_outer + 2 * segments
for i in range(segments):
    next_idx = (i + 1) % segments
    faces.append([offset_inner + i, offset_inner + next_idx, offset_inner + segments + i])
    faces.append([offset_inner + next_idx, offset_inner + segments + next_idx, offset_inner + segments + i])

# Create top and bottom faces for the main tube
for i in range(segments):
    next_idx = (i + 1) % segments
    # Bottom face (outer - inner, at base_height)
    faces.append([offset_outer + i, offset_inner + i, offset_inner + next_idx])
    faces.append([offset_outer + i, offset_inner + next_idx, offset_outer + next_idx])
    # Top face (outer - inner, at base_height + tube_height)
    faces.append([offset_outer + segments + i, offset_outer + segments + next_idx, offset_inner + segments + i])
    faces.append([offset_outer + segments + next_idx, offset_inner + segments + next_idx, offset_inner + segments + i])

# Convert to numpy array
faces = np.array(faces)

# Create STL mesh
final_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, face in enumerate(faces):
    for j in range(3):
        final_mesh.vectors[i][j] = vertices[face[j], :]

# Save to STL file
output_file = "tube_with_solid_base_corrected.stl"
final_mesh.save(output_file)

print(f"STL file has been saved as {output_file}")
