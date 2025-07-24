import torch
from transformers import pipeline
import base64
import io
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
        video_data = pipe(prompt, num_frames=8)
        buffer = io.BytesIO()
        for frame in video_data["frames"]:
            buffer.write(frame.tobytes())
        video_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return {"video_base64": video_b64}
    except Exception as e:
        return {"error": f"Video generation failed: {str(e)}"}

def health_check():
    try:
        _ = pipe("test prompt", num_frames=1)
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}