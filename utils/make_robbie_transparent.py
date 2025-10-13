#!/usr/bin/env python3
"""
Make Robbie images have transparent backgrounds instead of white
Select only frames where Robbie is touching his chin for smoother animation
Resize to 60x60 pixels
"""
from PIL import Image
import os

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
images_dir = os.path.join(project_root, 'images')

print("🎨 Making Robbie backgrounds transparent and resizing to 60x60...")

# Select frames where Robbie is touching his chin (consecutive for smooth animation)
# Based on the 3x3 grid, frames 4-6 (middle row) show the chin-touch gesture best
selected_frames = [4, 5, 6]  # Middle row - consistent chin-touching pose

for i, frame_num in enumerate(selected_frames, start=1):
    input_path = os.path.join(images_dir, f'robbie_{frame_num}_100x100.png')
    output_path = os.path.join(images_dir, f'robbie_anim_{i}.png')
    
    if not os.path.exists(input_path):
        print(f"  ⚠️  Frame {frame_num} not found, skipping...")
        continue
    
    # Load image
    img = Image.open(input_path).convert("RGBA")
    
    # Get pixel data
    datas = img.getdata()
    
    # Replace white/light backgrounds with transparency
    new_data = []
    for item in datas:
        # If pixel is white or very light (close to white), make it transparent
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            new_data.append((255, 255, 255, 0))  # Transparent
        else:
            new_data.append(item)  # Keep original
    
    # Update image data
    img.putdata(new_data)
    
    # Resize to 60x60
    img = img.resize((60, 60), Image.LANCZOS)
    
    # Save with transparency
    img.save(output_path, "PNG")
    print(f"  ✅ Created robbie_anim_{i}.png (from frame {frame_num}) - 60x60 with transparent background")

print(f"\n🎉 Created 3-frame animation with transparent backgrounds!")
print(f"📁 Location: {images_dir}")
print("\nNew files:")
for i in range(1, 4):
    print(f"  - robbie_anim_{i}.png")
