import torch
from transformers import pipeline

def load_video_model():
    try:
        pipe = pipeline(
            "text-to-video",
            model="Wan-AI/Wan2.1-T2V-14B",
            device="cuda" if torch.cuda.is_available() else "cpu"
        )
        return pipe
    except Exception as e:
        raise Exception(f"Failed to load video model: {str(e)}")

pipe = load_video_model()

def generate_video(prompt: str):
    try:
        video_frames = pipe(prompt)["frames"]
        return {"video_frames": video_frames}  # Simplified; actual encoding depends on output format
    except Exception as e:
        return {"error": f"Video generation failed: {str(e)}"}

def health_check():
    try:
        _ = pipe("test prompt", num_frames=1)
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}