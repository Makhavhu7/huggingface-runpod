from transformers import pipeline
import torch
import os

class VideoGenerator:
    def __init__(self):
        model_id = "Wan-AI/Wan2.1-T2V-14B"
        try:
            self.pipe = pipeline("text-to-video", model=model_id, device=0 if torch.cuda.is_available() else -1)
        except Exception as e:
            print(f"Error loading video model: {e}")
            self.pipe = None

    def generate(self, prompt, output_path="output_video.mp4"):
        if self.pipe is None:
            raise Exception("Video model not loaded")
        video = self.pipe(prompt)
        with open(output_path, "wb") as f:
            f.write(video["video"])
        return output_path

    def health_check(self):
        return self.pipe is not None