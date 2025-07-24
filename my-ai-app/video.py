import torch
from transformers import pipeline
import base64
import cv2
import numpy as np
import os

def load_video_model():
    try:
        pipe = pipeline(
            "text-to-video",
            model="Wan-AI/Wan2.1-T2V-14B",
            device="cuda" if torch.cuda.is_available() else "cpu",
            token=os.getenv("HUGGINGFACE_TOKEN")
        )
        return pipe
    except Exception as e:
        raise Exception(f"Failed to load video model: {str(e)}")

pipe = load_video_model()

def generate_video(prompt: str):
    try:
        video_frames = pipe(prompt, num_frames=16)["frames"]
        # Convert frames to base64-encoded video
        out = cv2.VideoWriter(
            "temp.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 24, (video_frames[0].shape[1], video_frames[0].shape[0])
        )
        for frame in video_frames:
            frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
            out.write(frame)
        out.release()
        with open("temp.mp4", "rb") as f:
            video_b64 = base64.b64encode(f.read()).decode("utf-8")
        return {"video_base64": video_b64}
    except Exception as e:
        return {"error": f"Video generation failed: {str(e)}"}

def health_check():
    try:
        _ = pipe("test prompt", num_frames=1)
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}