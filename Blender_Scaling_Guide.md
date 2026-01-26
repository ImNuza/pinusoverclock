# Blender 3D Model Scaling Guide for ArtSpace

This guide explains how to use Blender (a free 3D software) to correctly scale your 3D models so they appear at their real-world size in the ArtSpace AR viewer.

**Why is this necessary?** 3D models are often created without a specific real-world scale. To make the AR experience realistic, we need to ensure a model that is 1 meter tall in the real world is also 1 meter tall in the 3D file.

---

## 1. Download and Install Blender

If you don't have it, download Blender for free from the official website:

- **[Download Blender](https://www.blender.org/download/)** (Available for Windows, macOS, and Linux)

---

## 2. Manual Scaling (The Easy Way)

This method is best for scaling one model at a time.

### Step 1: Clean the Scene

- Open Blender.
- You will see a default cube, camera, and light. Select them all by pressing `A`.
- Press `X` and then click **Delete** to clear the scene.

### Step 2: Import Your GLB Model

- Go to **File > Import > gLTF 2.0 (.glb/.gltf)**.
- Navigate to your `.glb` file and select it.
- Click **Import gLTF 2.0**.

### Step 3: Set Scene Units to Meters

- In the right-hand properties panel, go to the **Scene Properties** tab (looks like a cone and a sphere).
- Expand the **Units** section.
- Make sure **Unit System** is set to **Metric** and **Length** is set to **Meters**.

### Step 4: Scale the Object

- Select your imported object by clicking on it in the viewport.
- Press `N` to open the Transform panel on the right side of the viewport.
- Look at the **Dimensions** values. These show the current size of your object in meters.
- **Adjust the dimensions** to match the real-world size of your artwork. For example, if your artwork is 80cm tall, set the Z (height) dimension to `0.8`.
- **Important:** Make sure the little padlock icon next to the dimensions is **locked**. This will ensure the object scales proportionally.

![Blender Dimensions Panel](https://i.imgur.com/your_image_link_here.png) *<-- I will generate a proper image for this later if needed.*

### Step 5: Apply the Scale

- With the object still selected, press `Ctrl + A` (or `Cmd + A` on Mac).
- A menu will pop up. Select **Scale**.
- This "bakes" the new scale into the model, making it the new default (1, 1, 1).

### Step 6: Export the Scaled Model

- Go to **File > Export > gLTF 2.0 (.glb/.gltf)**.
- In the export settings on the right:
    - **Format**: Choose **gLTF Binary (.glb)**.
    - **Include**: Check **Selected Objects**.
    - **Transform**: Make sure **+Y Up** is checked.
    - **Geometry**: Under **Apply Modifiers**, make sure it's checked.
- Name your file (e.g., `MyArtwork_scaled.glb`) and click **Export gLTF 2.0**.

Your new `.glb` file is now correctly scaled and ready to be uploaded to ArtSpace!

---

## 3. Automated Scaling with a Python Script (The Advanced Way)

If you have many models to process, you can use this Python script inside Blender.

### How to Use the Script:

1.  Open Blender.
2.  Go to the **Scripting** workspace tab at the top.
3.  Click **New** to create a new text block.
4.  Copy and paste the Python script from `scaling_script.py` in this project into the text editor.
5.  **Edit the script variables** at the top:
    - `INPUT_FOLDER`: The absolute path to the folder containing your source `.glb` files.
    - `OUTPUT_FOLDER`: The absolute path to where you want to save the scaled files.
    - `TARGET_HEIGHT_METERS`: The desired height for all models in meters.
6.  Click the **Run Script** button (play icon) in the scripting workspace.

Blender will automatically open each file, scale it to the target height, and export it to your output folder.

**Note:** This script assumes you want all models to have the same height. For different sizes, the manual method is better.
