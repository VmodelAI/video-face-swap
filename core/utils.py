import os
import shutil
import subprocess
from io import BytesIO
from pathlib import Path
import imageio

from PIL import Image
import numpy as np

import requests


def path(string):
    return string


def detect_fps(input_path):
    input_path = path(input_path)
    output = os.popen(
        f'ffprobe -v error -select_streams v -of default=noprint_wrappers=1:nokey=1 -show_entries stream=r_frame_rate "{input_path}"').read()
    if "/" in output:
        try:
            return int(output.split("/")[0]) // int(output.split("/")[1])
        except:
            pass
    return 60


def set_fps(input_path, output_path, fps):
    input_path, output_path = path(input_path), path(output_path)
    os.system(f'ffmpeg -i "{input_path}" -filter:v fps=fps={fps} "{output_path}"')


def create_video(video_name, fps, output_dir):
    output_dir = path(output_dir)
    os.system(
        f'ffmpeg -framerate {fps} -i "{output_dir}/%04d.png" -c:v libx264 -pix_fmt yuv420p -y "{output_dir}/output.mp4"')
    return output_dir + f"/output.mp4"


def extract_frames(input_path, output_dir):
    input_path = Path(input_path)
    output_dir = Path(output_dir)

    # Ensure the output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Use subprocess to call ffmpeg, with hardware acceleration if available, without changing the frame rate
    command = [
        'ffmpeg',
        '-hwaccel', 'cuda',  # This line can be removed if GPU acceleration is not available
        '-i', str(input_path),
        f'{output_dir}/%04d.png'  # Change the output format to png
    ]

    try:
        subprocess.run(command, check=True)
        print("Frames extracted successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")


from pathlib import Path
from PIL import Image


def add_audio(output_dir, target_path, keep_frames):
    video = target_path.split("/")[-1]
    video_name = video.split(".")[0]
    save_to = output_dir + f"/swapped-" + video_name + ".mp4"
    save_to_ff, output_dir_ff = path(save_to), path(output_dir)
    os.system(
        f'ffmpeg -i "{output_dir_ff}/output.mp4" -i "{output_dir_ff}/{video}" -c:v copy -map 0:v:0 -map 1:a:0 -y "{save_to_ff}"')
    if not os.path.isfile(save_to):
        shutil.move(output_dir + f"/output.mp4", save_to)
    if not keep_frames:
        shutil.rmtree(output_dir)
    return save_to


def add_white_side(input_image_path):
    # Add a white border to the image
    temp_output_path = input_image_path + "_temp.png"  # Temporary output file
    try:
        command_parts = [
            "ffmpeg",
            "-i",
            input_image_path,
            "-vf",
            "pad=width=ceil(iw*1.5):height=ceil(ih*1.5):x=(ceil(iw*0.25)):y=(ceil(ih*0.25)):color=white",
            "-y",
            temp_output_path  # Output to a temporary file
        ]
        subprocess.run(command_parts, check=True)
        print(f'Successfully added white border to image: {input_image_path}')
        shutil.move(temp_output_path, input_image_path)  # Overwrite the original file with the temporary file
        return input_image_path
    except Exception as e:
        print(f"Failed to add white border to image: {e}")
        return input_image_path


def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)


# Adjust video dimensions-----------start
def get_video_dimensions(input_path):
    input_path = Path(input_path)
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of',
             'csv=p=0:s=x', str(input_path)],
            capture_output=True, text=True, check=True
        )
        output = result.stdout.strip()
        if "x" in output:
            try:
                width, height = map(int, output.split('x'))
                return width, height
            except ValueError:
                pass
    except subprocess.CalledProcessError as e:
        print(f"Error running ffprobe: {e}")
    return None, None


def get_webp_dimensions(url):
    # Get image dimensions for webp, gif
    # Download the WebP image from the URL
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))

    # Get the width and height of the image
    width, height = image.size
    return width, height


def adjust_to_even(value):
    return value if value % 2 == 0 else value - 1 if value > 1 else 2


def adjust_video_dimensions(input_path, output_path):
    # Ensure width and height are even numbers
    input_path = Path(input_path)
    output_path = Path(output_path)

    try:
        width, height = get_video_dimensions(input_path)

        if width is None or height is None:
            raise ValueError("Could not get video width and height information")

        # Check if dimensions need to be adjusted
        if width % 2 == 0 and height % 2 == 0:
            print("Width and height are already even, no adjustment needed")
            return str(input_path)

        new_width = adjust_to_even(width)
        new_height = adjust_to_even(height)

        subprocess.run(
            ['ffmpeg', '-i', str(input_path), '-vf', f"scale={new_width}:{new_height}", '-c:a', 'copy',
             str(output_path)],
            check=True
        )
        print(f'Video dimensions adjusted, w:{new_height},h{new_height}')
        return str(output_path)
    except Exception as e:
        print(f"check video size error: {e}")
        return str(input_path)

# Adjust video dimensions-----------end