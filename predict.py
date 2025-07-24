# Prediction interface for Cog ⚙️
# https://github.com/replicate/cog/blob/main/docs/python.md
import uuid

from cog import BasePredictor, Input
from cog import Path as CogPath
import sys
import time
import torch
import core.model_manager
import core.globals
from core.face_swap_video import faceSwapVideo

if not torch.cuda.is_available():
    core.globals.providers = ['CPUExecutionProvider']
    print("No GPU detected. Using CPU instead.")

import cv2
from typing import Iterator
from subprocess import call, check_call

from core.utils import add_white_side
from core.config import get_face


def status(string):
    print("Status: " + string)


def run_cmd(command):
    try:
        call(command, shell=True)
    except KeyboardInterrupt:
        print("Process interrupted")
        sys.exit(1)


class Predictor(BasePredictor):
    def setup(self):
        # HACK: wait a little bit for instance to be ready
        time.sleep(10)
        check_call("nvidia-smi", shell=True)
        assert torch.cuda.is_available()

    def predict(
            self,
            source: CogPath = Input(description="Source", default=None),
            target: CogPath = Input(description="Target", default=None),
            face_enhance: bool = Input(description="face_enhance", default=False),
            keep_fps: bool = Input(description="Keep FPS", default=True),
            keep_frames: bool = Input(description="Keep Frames", default=True),
    ) -> Iterator[CogPath]:

        source = str(source)
        target = str(target)

        # Validation
        source_face = get_face(cv2.imread(source))
        if not source:
            print("\n[WARNING] No face detected in source image. Please try with another one.\n")
            return

        # Add white padding to the input image
        source = add_white_side(source)

        # Face swap in video
        output = faceSwapVideo.swap(target=target, source=source, keep_fps=keep_fps, keep_frames=keep_frames,
                                    is_enhancer=face_enhance)
        yield CogPath(output)
        status("video swap successful!")
        return