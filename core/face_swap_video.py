import glob
import os
import shutil
import time
from pathlib import Path

from core.processor import process_video
from core.utils import detect_fps, set_fps, adjust_video_dimensions, extract_frames, create_video, add_audio


class FaceSwapVideo:
    def swap(self, target, source, keep_fps, keep_frames, video_name="output.mp4", output_dir="./output",
             is_enhancer=False):
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        Path(output_dir).mkdir(exist_ok=True)

        # Check video frame rate
        print("Checking video frame rate...")
        fps = detect_fps(target)

        if not keep_fps and fps > 30:
            this_path = output_dir + "/" + video_name + ".mp4"
            set_fps(target, this_path, 30)
            target, fps = this_path, 30
        else:
            shutil.copy(target, output_dir)

        new_path = output_dir + "/" + video_name + ".mp4"
        target = adjust_video_dimensions(target, new_path)

        # Extracting video frames
        print("Extracting video frames...")
        extract_frames(target, output_dir)
        frame_paths = tuple(sorted(
            glob.glob(output_dir + f"/*.png"),
            key=lambda x: int(x.split("/")[-1].replace(".png", ""))
        ))

        # Swapping faces
        print("Swapping faces...")
        start_time = time.time()
        process_video(source, frame_paths, is_enhancer)
        end_time = time.time()
        print(f"Face swapping took: {end_time - start_time:.2f} s")

        # Merging video
        print("Merging video...")
        output_file = create_video(video_name, fps, output_dir)

        # Adding audio
        print("Adding audio...")
        output_file = add_audio(output_dir, target, keep_frames)
        print("\n\nVideo has been generated:", output_file, "\n\n")

        return output_file


faceSwapVideo = FaceSwapVideo()