#!/usr/bin/env python3
"""
Create GLB files for 2D paintings with embedded textures.
Each painting becomes a flat 3D plane that can be viewed in AR.
"""

import struct
import json
import base64
import os
from PIL import Image
import io

def create_painting_glb(image_path, output_path, width_cm, height_cm):
    """
    Create a GLB file for a painting with the image as a texture.
    
    Args:
        image_path: Path to the painting image
        output_path: Path for the output GLB file
        width_cm: Width in centimeters
        height_cm: Height in centimeters
    """
    
    # Convert cm to meters for glTF (1 unit = 1 meter)
    width_m = width_cm / 100.0
    height_m = height_cm / 100.0
    
    # Half dimensions for vertex positions (centered at origin)
    hw = width_m / 2
    hh = height_m / 2
    depth = 0.02  # 2cm depth for the frame
    
    # Load and process image
    img = Image.open(image_path)
    
    # Resize if too large (max 1024px for mobile performance)
    max_size = 1024
    if img.width > max_size or img.height > max_size:
        ratio = min(max_size / img.width, max_size / img.height)
        new_size = (int(img.width * ratio), int(img.height * ratio))
        img = img.resize(new_size, Image.LANCZOS)
    
    # Convert to RGB if necessary
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Save image to bytes as JPEG
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='JPEG', quality=85)
    img_bytes = img_buffer.getvalue()
    
    # Create vertices for a flat plane (front face only for painting)
    # Positions: 4 corners of the painting
    positions = [
        -hw, -hh, 0,  # bottom-left
         hw, -hh, 0,  # bottom-right
         hw,  hh, 0,  # top-right
        -hw,  hh, 0,  # top-left
    ]
    
    # Normals: all pointing forward (Z+)
    normals = [
        0, 0, 1,
        0, 0, 1,
        0, 0, 1,
        0, 0, 1,
    ]
    
    # Texture coordinates (UV)
    texcoords = [
        0, 1,  # bottom-left
        1, 1,  # bottom-right
        1, 0,  # top-right
        0, 0,  # top-left
    ]
    
    # Indices for two triangles
    indices = [0, 1, 2, 0, 2, 3]
    
    # Pack binary data
    positions_bytes = struct.pack(f'{len(positions)}f', *positions)
    normals_bytes = struct.pack(f'{len(normals)}f', *normals)
    texcoords_bytes = struct.pack(f'{len(texcoords)}f', *texcoords)
    indices_bytes = struct.pack(f'{len(indices)}H', *indices)
    
    # Calculate buffer offsets
    positions_offset = 0
    positions_length = len(positions_bytes)
    
    normals_offset = positions_offset + positions_length
    normals_length = len(normals_bytes)
    
    texcoords_offset = normals_offset + normals_length
    texcoords_length = len(texcoords_bytes)
    
    indices_offset = texcoords_offset + texcoords_length
    indices_length = len(indices_bytes)
    
    # Combine geometry buffer
    geometry_buffer = positions_bytes + normals_bytes + texcoords_bytes + indices_bytes
    
    # Image buffer starts after geometry
    image_offset = len(geometry_buffer)
    image_length = len(img_bytes)
    
    # Total buffer
    total_buffer = geometry_buffer + img_bytes
    
    # Pad to 4-byte alignment
    padding = (4 - (len(total_buffer) % 4)) % 4
    total_buffer += b'\x00' * padding
    
    # Create glTF JSON
    gltf = {
        "asset": {
            "version": "2.0",
            "generator": "ArtSpace Painting Generator"
        },
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{
            "mesh": 0,
            "name": "Painting"
        }],
        "meshes": [{
            "primitives": [{
                "attributes": {
                    "POSITION": 0,
                    "NORMAL": 1,
                    "TEXCOORD_0": 2
                },
                "indices": 3,
                "material": 0
            }]
        }],
        "accessors": [
            {
                "bufferView": 0,
                "componentType": 5126,  # FLOAT
                "count": 4,
                "type": "VEC3",
                "min": [-hw, -hh, 0],
                "max": [hw, hh, 0]
            },
            {
                "bufferView": 1,
                "componentType": 5126,
                "count": 4,
                "type": "VEC3"
            },
            {
                "bufferView": 2,
                "componentType": 5126,
                "count": 4,
                "type": "VEC2"
            },
            {
                "bufferView": 3,
                "componentType": 5123,  # UNSIGNED_SHORT
                "count": 6,
                "type": "SCALAR"
            }
        ],
        "bufferViews": [
            {"buffer": 0, "byteOffset": positions_offset, "byteLength": positions_length, "target": 34962},
            {"buffer": 0, "byteOffset": normals_offset, "byteLength": normals_length, "target": 34962},
            {"buffer": 0, "byteOffset": texcoords_offset, "byteLength": texcoords_length, "target": 34962},
            {"buffer": 0, "byteOffset": indices_offset, "byteLength": indices_length, "target": 34963},
            {"buffer": 0, "byteOffset": image_offset, "byteLength": image_length}
        ],
        "buffers": [{
            "byteLength": len(total_buffer)
        }],
        "materials": [{
            "pbrMetallicRoughness": {
                "baseColorTexture": {"index": 0},
                "metallicFactor": 0,
                "roughnessFactor": 0.8
            },
            "doubleSided": True
        }],
        "textures": [{
            "sampler": 0,
            "source": 0
        }],
        "samplers": [{
            "magFilter": 9729,  # LINEAR
            "minFilter": 9987,  # LINEAR_MIPMAP_LINEAR
            "wrapS": 33071,     # CLAMP_TO_EDGE
            "wrapT": 33071
        }],
        "images": [{
            "bufferView": 4,
            "mimeType": "image/jpeg"
        }]
    }
    
    # Convert JSON to bytes
    json_str = json.dumps(gltf, separators=(',', ':'))
    json_bytes = json_str.encode('utf-8')
    
    # Pad JSON to 4-byte alignment
    json_padding = (4 - (len(json_bytes) % 4)) % 4
    json_bytes += b' ' * json_padding
    
    # Create GLB file
    # GLB Header (12 bytes)
    glb_header = struct.pack('<4sII', b'glTF', 2, 12 + 8 + len(json_bytes) + 8 + len(total_buffer))
    
    # JSON chunk
    json_chunk_header = struct.pack('<II', len(json_bytes), 0x4E4F534A)  # JSON
    
    # Binary chunk
    bin_chunk_header = struct.pack('<II', len(total_buffer), 0x004E4942)  # BIN
    
    # Write GLB file
    with open(output_path, 'wb') as f:
        f.write(glb_header)
        f.write(json_chunk_header)
        f.write(json_bytes)
        f.write(bin_chunk_header)
        f.write(total_buffer)
    
    print(f"Created: {output_path} ({os.path.getsize(output_path) / 1024:.1f} KB)")

# Define paintings to convert
paintings = [
    ("images/starry_night.jpg", "models/painting_starry_night.glb", 92, 73),
    ("images/monet_water_lilies.jpg", "models/painting_water_lilies.glb", 100, 100),
    ("images/van_gogh_cafe.jpg", "models/painting_cafe_terrace.glb", 81, 65),
    ("images/mona_lisa.jpg", "models/painting_mona_lisa.glb", 53, 77),
    ("images/kandinsky_improvisation_4.jpg", "models/painting_kandinsky.glb", 108, 158),
    ("images/abstract_blue.jpg", "models/painting_abstract_blue.glb", 80, 60),
    ("images/abstract_colorful.jpg", "models/painting_abstract_colorful.glb", 70, 50),
    ("images/abstract_gold.jpg", "models/painting_abstract_gold.glb", 90, 60),
    ("images/botanical_art.jpg", "models/painting_botanical.glb", 50, 70),
    ("images/classic_portrait.jpg", "models/painting_classic_portrait.glb", 60, 80),
    ("images/japanese_art.jpg", "models/painting_japanese.glb", 100, 50),
    ("images/minimalist_lines.jpg", "models/painting_minimalist.glb", 40, 60),
    ("images/modern_geometric.jpg", "models/painting_geometric.glb", 60, 60),
    ("images/neon_art.jpg", "models/painting_neon.glb", 50, 70),
    ("images/oil_painting.jpg", "models/painting_oil_landscape.glb", 120, 80),
]

if __name__ == "__main__":
    os.chdir("/home/ubuntu/pinusoverclock")
    
    for image_path, output_path, width, height in paintings:
        if os.path.exists(image_path):
            try:
                create_painting_glb(image_path, output_path, width, height)
            except Exception as e:
                print(f"Error processing {image_path}: {e}")
        else:
            print(f"Image not found: {image_path}")
    
    print("\nDone! All painting GLB files created.")
