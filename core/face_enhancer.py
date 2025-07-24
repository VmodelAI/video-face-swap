import threading
import gfpgan
import os
from insightface.app.common import Face


class FaceEnhancer:
    def __init__(self, model_path, upscale=1):
        if not os.path.isfile(model_path):
            raise FileNotFoundError(f'File "{model_path}" does not exist!')

        self.model_path = model_path
        self.upscale = upscale
        self.face_enhancer = gfpgan.GFPGANer(model_path=self.model_path, upscale=self.upscale)
        self.semaphore = threading.Semaphore()

    def process_frame(self, temp_frame):
        with self.semaphore:
            _, _, enhanced_frame = self.face_enhancer.enhance(temp_frame, paste_back=True)
        return enhanced_frame

    def enhancer_image(self, target_path):
        try:
            result = self.process_frame(target_path)
            return result
        except Exception as e:
            print(f'Error processing image: {e}')
            return None


face_enhancer = FaceEnhancer("GFPGANv1.4.pth", upscale=1)
