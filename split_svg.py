import re

with open('t:/Vaastu Next/lotus.svg', 'r') as f:
    content = f.read()

# Find the path d attribute
match = re.search(r'd="([^"]+)"', content)
if not match:
    print("No path d found")
    exit(1)

d_data = match.group(1)
# Split by M
sub_paths = d_data.split('M')
lotus_subpaths = []
text_subpaths = []

for part in sub_paths:
    if not part.strip():
        continue
    path_str = 'M' + part
    # Find all numbers
    coords = re.findall(r'[-+]?\d*\.\d+|\d+', part)
    if coords:
        y = float(coords[1])
        if y < 290:
            lotus_subpaths.append(path_str)
        else:
            text_subpaths.append(path_str)

lotus_d = ' '.join(lotus_subpaths)

# Calculate bounding box of the lotus paths
all_coords = re.findall(r'[-+]?\d*\.\d+|\d+', lotus_d)
xs = [float(all_coords[i]) for i in range(0, len(all_coords), 2)]
ys = [float(all_coords[i]) for i in range(1, len(all_coords), 2)]

min_x, max_x = min(xs), max(xs)
min_y, max_y = min(ys), max(ys)
width = max_x - min_x
height = max_y - min_y

print(f"Bounding Box: min_x={min_x}, min_y={min_y}, max_x={max_x}, max_y={max_y}")
print(f"Width={width}, Height={height}")

# Create cropped SVG with viewBox centered on the lotus with small padding
padding = 5
view_box = f"{min_x - padding} {min_y - padding} {width + 2*padding} {height + 2*padding}"

lotus_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view_box}">
  <path d="{lotus_d}" fill="currentColor" />
</svg>'''

with open('t:/Vaastu Next/lotus_only.svg', 'w') as f:
    f.write(lotus_svg)

print("Saved lotus_only.svg!")
