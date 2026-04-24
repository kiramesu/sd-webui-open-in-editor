import os
import subprocess
import urllib.parse  # Added: standard library to decode URL encoding (such as %20) back to original form
from fastapi import FastAPI, Body
from modules import script_callbacks, shared

# Function to open an image with external software
def open_image_in_editor(image_path: str, original_url: str):
    # Get the .exe path from settings and remove surrounding quotes
    editor_path = shared.opts.data.get("editor_executable_path", "")
    if editor_path:
        editor_path = editor_path.strip('\"\'')
    
    if not editor_path or not os.path.exists(editor_path):
        return {"status": "error", "message": f"The correct paint software path is not set in Settings. Detected path: {editor_path}"}

    # [Change] On error, display in a popup which path Python attempted to access and failed
    if not os.path.exists(image_path):
        return {
            "status": "error", 
            "message": f"Image file not found.\n[Checked path]: {image_path}\n[Original URL]: {original_url}"
        }

    try:
        # Launch the process in the background
        subprocess.Popen([editor_path, image_path])
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Add a custom endpoint to FastAPI (communication interface from JS)
def on_app_started(block, app: FastAPI):
    @app.post("/custom/open-in-editor")
    def api_open_in_editor(image_path: str = Body(..., embed=True)):
        # 1. Decode URL encoding (such as %20) back to spaces, etc.
        decoded_url = urllib.parse.unquote(image_path)
        
        # 2. Remove unnecessary parts like http://.../file= and extract only the local path
        clean_path = decoded_url
        if "file=" in clean_path:
            clean_path = clean_path.split("file=")[-1]
        elif "filename=" in clean_path: # Handle different WebUI versions
            clean_path = clean_path.split("filename=")[-1]
            
        # 3. Remove any trailing parameters such as ?xxx if present
        clean_path = clean_path.split("?")[0]
        
        return open_image_in_editor(clean_path, image_path)

# Add settings items to the Settings tab
def on_ui_settings():
    section = ("open_in_editor", "Paint software")
    shared.opts.add_option(
        "editor_executable_path",
        shared.OptionInfo(
            "",
            "Path to the paint software executable (e.g.: C:\\Program Files\\Adobe\\Adobe Photoshop 2024\\Photoshop.exe)",
            section=section
        )
    )

script_callbacks.on_app_started(on_app_started)
script_callbacks.on_ui_settings(on_ui_settings)
