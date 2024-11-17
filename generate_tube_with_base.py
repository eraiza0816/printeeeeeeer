import numpy as np
from stl import mesh

# Parameters
outer_radius = 9.7 / 2  # mm
inner_radius = 7.8 / 2  # mm
height = 3.5  # mm
base_radius = 12 / 2  # mm (底面円の直径12mm)
base_height = 1.0  # mm (底面円の高さ)
segments = 100  # Number of segments for smooth circular shape

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

# Generate vertices for the main tube
outer_bottom, outer_top = create_cylinder(outer_radius, height, segments)
inner_bottom, inner_top = create_cylinder(inner_radius, height - 0.5, segments, z_offset=0.5)  # Indentation

# Generate vertices for the base
base_bottom, base_top = create_cylinder(base_radius, base_height, segments)

# Combine all vertices
vertices = np.vstack((outer_bottom, outer_top, inner_bottom, inner_top, base_bottom, base_top))

# Create faces
faces = []

# Create outer wall faces for the main tube
for i in range(segments):
    next_idx = (i + 1) % segments
    faces.append([i, next_idx, segments + i])  # Bottom to top
    faces.append([next_idx, segments + next_idx, segments + i])

# Create inner wall faces for the main tube
offset_inner = 2 * segments
for i in range(segments):
    next_idx = (i + 1) % segments
    faces.append([offset_inner + i, offset_inner + next_idx, offset_inner + segments + i])
    faces.append([offset_inner + next_idx, offset_inner + segments + next_idx, offset_inner + segments + i])

# Create top and bottom faces for the main tube
for i in range(segments):
    next_idx = (i + 1) % segments
    # Bottom face (outer - inner)
    faces.append([i, offset_inner + i, offset_inner + next_idx])
    faces.append([i, offset_inner + next_idx, next_idx])
    # Top face (outer - inner)
    faces.append([segments + i, segments + next_idx, offset_inner + segments + i])
    faces.append([segments + next_idx, offset_inner + segments + next_idx, offset_inner + segments + i])

# Create faces for the base
offset_base = 4 * segments
for i in range(segments):
    next_idx = (i + 1) % segments
    # Connect base to the outer wall of the tube
    faces.append([offset_base + i, offset_base + next_idx, i])
    # Create base faces (top circle of base)
    faces.append([offset_base + i, offset_base + next_idx, offset_base + segments + i])

# Convert to numpy array
faces = np.array(faces)

# Create STL mesh
tube_with_base_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, face in enumerate(faces):
    for j in range(3):
        tube_with_base_mesh.vectors[i][j] = vertices[face[j], :]

# Save to STL file
output_file = "tube_with_base_model.stl"
tube_with_base_mesh.save(output_file)

print(f"STL file has been saved as {output_file}")
