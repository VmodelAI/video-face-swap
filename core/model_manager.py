# /src/core/model_manager.py

import os
import subprocess

# Define the models that need to be checked and downloaded
MODELS_TO_CHECK = {
    "GFPGANv1.4.pth": "https://huggingface.co/gmk123/GFPGAN/resolve/main/GFPGANv1.4.pth",
    "inswapper_128.onnx": "https://huggingface.co/xingren23/comfyflow-models/resolve/976de8449674de379b02c144d0b3cfa2b61482f2/insightface/inswapper_128.onnx"
}

# Specify the target directory for downloads (root directory)
TARGET_DIRECTORY = "/"


def run_cmd(command):
    """A simple helper function to execute shell commands and print information."""
    try:
        print(f"Executing command: {command}")
        subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Command execution failed!")
        print(f"Error code: {e.returncode}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        raise e


def ensure_models_exist():
    """
    Checks if all required model files exist in the target directory.
    If a file does not exist, it will be downloaded using wget.
    """
    print("Starting to check for all required model files...")

    for filename, url in MODELS_TO_CHECK.items():
        # Construct the full path for the file
        file_path = os.path.join(TARGET_DIRECTORY, filename)

        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"File '{file_path}' does not exist, downloading...")
            # Build the wget command, the -O parameter specifies the output path
            command = f"wget -O {file_path} '{url}'"
            try:
                run_cmd(command)
                print(f"File '{filename}' has been successfully downloaded to '{TARGET_DIRECTORY}'")
            except Exception as e:
                print(f"Failed to download '{filename}', please check the network or URL. Error: {e}")
                # If the download fails, you can choose to raise an exception to interrupt the startup process
                raise SystemExit(f"Critical model download failed: {filename}")
        else:
            print(f"File '{file_path}' already exists, skipping download.")

    print("All model files have been checked.")

# This line executes the check when the script is imported.
ensure_models_exist()