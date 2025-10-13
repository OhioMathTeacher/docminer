#!/usr/bin/env python3
"""
Split robbie_panel.png into 9 individual animation frames (3x3 grid)
"""
from PIL import Image
import os

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
panel_path = os.path.join(project_root, 'images', 'robbie_panel.png')
output_dir = os.path.join(project_root, 'images')

print(f"🎨 Splitting Robbie panel into 9 animation frames...")
print(f"📂 Input: {panel_path}")

# Load the panel
panel = Image.open(panel_path)
panel_width, panel_height = panel.size
print(f"📐 Panel size: {panel_width}x{panel_height}")

# Calculate frame size (panel is 3x3 grid)
frame_width = panel_width // 3
frame_height = panel_height // 3
print(f"📐 Each frame: {frame_width}x{frame_height}")

# Extract each frame
frame_num = 1
for row in range(3):
    for col in range(3):
        # Calculate crop box (left, top, right, bottom)
        left = col * frame_width
        top = row * frame_height
        right = left + frame_width
        bottom = top + frame_height
        
        # Crop the frame
        frame = panel.crop((left, top, right, bottom))
        
        # Resize to 100x100 for consistency with existing frames
        frame_resized = frame.resize((100, 100), Image.Resampling.LANCZOS)
        
        # Save
        output_path = os.path.join(output_dir, f'robbie_{frame_num}_100x100.png')
        frame_resized.save(output_path, 'PNG', optimize=True)
        
        print(f"  ✅ Frame {frame_num}: robbie_{frame_num}_100x100.png (row {row}, col {col})")
        frame_num += 1

print(f"\n🎉 Successfully created 9 Robbie animation frames!")
print(f"📁 Location: {output_dir}")
print(f"\nFiles created:")
for i in range(1, 10):
    print(f"  - robbie_{i}_100x100.png")
