import bpy
import os

# --- CONFIGURATION ---
# Set the path to the folder containing your .glb files
INPUT_FOLDER = "/path/to/your/models"

# Set the path to the folder where you want to save the scaled .glb files
OUTPUT_FOLDER = "/path/to/your/scaled_models"

# Set the target height for all models in meters
# For example, 0.8 means 80cm tall
TARGET_HEIGHT_METERS = 0.8

# --- SCRIPT --- (Do not edit below this line)

def scale_and_export(input_path, output_path, target_height):
    # Clean the scene
    bpy.ops.object.select_all(action=\'SELECT\')
    bpy.ops.object.delete()

    # Import the GLB file
    bpy.ops.import_scene.gltf(filepath=input_path)

    # Get the imported object (assumes one main object)
    imported_obj = bpy.context.selected_objects[0]
    
    # Ensure it is the active object
    bpy.context.view_layer.objects.active = imported_obj

    # Calculate the scaling factor
    current_height = imported_obj.dimensions.z
    if current_height == 0:
        print(f"Skipping {input_path} because its height is 0.")
        return
        
    scale_factor = target_height / current_height

    # Apply the scale
    imported_obj.scale = (scale_factor, scale_factor, scale_factor)
    
    # Apply the scale transform
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # Export the scaled model
    bpy.ops.export_scene.gltf(
        filepath=output_path,
        export_format=\'GLB\',
        use_selection=True,
        export_apply=True
    )
    print(f"Successfully scaled and exported {output_path}")


def main():
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith(".glb"):
            input_file_path = os.path.join(INPUT_FOLDER, filename)
            output_file_path = os.path.join(OUTPUT_FOLDER, filename)
            
            try:
                scale_and_export(input_file_path, output_file_path, TARGET_HEIGHT_METERS)
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Run the script
if __name__ == "__main__":
    main()
