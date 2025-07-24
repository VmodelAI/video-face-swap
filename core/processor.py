import os

import cv2
import insightface
import torch

import core.globals
from core.config import get_face
from core.face_enhancer import face_enhancer
from core.utils import rreplace

if os.path.isfile('inswapper_128.onnx'):
    face_swapper = insightface.model_zoo.get_model('inswapper_128.onnx', providers=core.globals.providers)
else:
    quit('File "inswapper_128.onnx" does not exist!')


def process_video(source_img, frame_paths, is_enhancer=False):
    """
    Sequentially processes video frames using a single thread.
    """
    # 1. Get the face from the source image
    try:
        source_face = get_face(cv2.imread(source_img))
        if not source_face:
            # Error: No face detected in the source image, terminating the program.
            print("Error: No face detected in the source image, terminating the program.")
            return
    except Exception as e:
        # Error reading the source image: {e}
        print(f"Error reading source image: {e}")
        return

    total_frames = len(frame_paths)
    # Starting to sequentially process {total_frames} frames...
    print(f"Starting to sequentially process {total_frames} frames...")

    # 2. Use a simple for loop to iterate and process each frame
    for index, frame_path in enumerate(frame_paths):
        try:
            frame = cv2.imread(frame_path)
            # Check if the image was loaded successfully
            if frame is None:
                # Warning: Could not read frame {frame_path}, skipping.
                print(f"\nWarning: Could not read frame {frame_path}, skipping.")
                continue

            # Get the face from the current frame
            face = get_face(frame)

            if face:
                # Perform face swap
                result = face_swapper.get(frame, face, source_face, paste_back=True)

                # If needed, perform enhancement
                if is_enhancer:
                    result = face_enhancer.enhancer_image(result)

                # Save the processed frame
                cv2.imwrite(frame_path, result)

                # Print a progress dot
                print('.', end='', flush=True)
            else:
                # If no face is detected, print 'S' (Skip)
                print('S', end='', flush=True)

            # Clear CUDA cache, helps to stabilize VRAM usage when processing many images
            torch.cuda.empty_cache()

        except Exception as e:
            # If an error occurs while processing a single frame, print the error and continue to the next frame
            print(f'\nAn error occurred while processing frame {frame_path}: {e}')

    # All frames processed.
    print("\n\nAll frames have been processed.")


def process_img(source_img, target_path):
    frame = cv2.imread(target_path)
    face = get_face(frame)
    source_face = get_face(cv2.imread(source_img))
    result = face_swapper.get(frame, face, source_face, paste_back=True)
    target_path = rreplace(target_path, "/", "/swapped-", 1) if "/" in target_path else "swapped-" + target_path
    print(target_path)
    cv2.imwrite(target_path, result)
    return target_path