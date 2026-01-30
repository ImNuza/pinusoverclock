#!/usr/bin/env python3
"""
Create a simple picture frame GLB model for 2D artwork display in AR.
The frame is a flat plane that can display artwork images.
"""

import numpy as np
import trimesh
import os

def create_picture_frame(width=1.0, height=0.75, frame_thickness=0.05, frame_depth=0.02):
    """
    Create a picture frame mesh with a flat canvas area.
    
    Args:
        width: Width of the artwork area in meters
        height: Height of the artwork area in meters
        frame_thickness: Thickness of the frame border
        frame_depth: Depth/thickness of the frame
    """
    
    # Create the main canvas (flat plane for the artwork)
    canvas = trimesh.creation.box(extents=[width, height, 0.001])
    canvas.visual.face_colors = [200, 200, 200, 255]  # Light gray placeholder
    
    # Create frame pieces (4 borders)
    frame_color = [60, 40, 20, 255]  # Dark wood color
    
    # Top frame piece
    top = trimesh.creation.box(extents=[width + 2*frame_thickness, frame_thickness, frame_depth])
    top.apply_translation([0, (height + frame_thickness) / 2, frame_depth/2])
    top.visual.face_colors = frame_color
    
    # Bottom frame piece
    bottom = trimesh.creation.box(extents=[width + 2*frame_thickness, frame_thickness, frame_depth])
    bottom.apply_translation([0, -(height + frame_thickness) / 2, frame_depth/2])
    bottom.visual.face_colors = frame_color
    
    # Left frame piece
    left = trimesh.creation.box(extents=[frame_thickness, height, frame_depth])
    left.apply_translation([-(width + frame_thickness) / 2, 0, frame_depth/2])
    left.visual.face_colors = frame_color
    
    # Right frame piece
    right = trimesh.creation.box(extents=[frame_thickness, height, frame_depth])
    right.apply_translation([(width + frame_thickness) / 2, 0, frame_depth/2])
    right.visual.face_colors = frame_color
    
    # Combine all pieces
    frame = trimesh.util.concatenate([canvas, top, bottom, left, right])
    
    return frame

def main():
    # Create frames in different aspect ratios
    frames = {
        'frame_landscape.glb': (1.0, 0.75),   # 4:3 landscape
        'frame_portrait.glb': (0.75, 1.0),    # 3:4 portrait
        'frame_square.glb': (0.8, 0.8),       # 1:1 square
        'frame_wide.glb': (1.2, 0.6),         # 2:1 wide/panoramic
    }
    
    output_dir = '/home/ubuntu/pinusoverclock/models'
    
    for filename, (w, h) in frames.items():
        frame = create_picture_frame(width=w, height=h)
        output_path = os.path.join(output_dir, filename)
        frame.export(output_path)
        print(f"Created {filename} ({w}m x {h}m)")
    
    print("\nAll frames created successfully!")

if __name__ == '__main__':
    main()
