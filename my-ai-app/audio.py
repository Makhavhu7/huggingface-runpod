import torch
from transformers import pipeline
import base64
import io
import os

def load_audio_model():
    try:
        pipe = pipeline(
            "text-to-speech",
            model="suno/bark",
            device="cuda" if torch.cuda.is_available() else "cpu",
            token=os.getenv("HUGGINGFACE_TOKEN")
        )
        return pipe
    except Exception as e:
        raise Exception(f"Failed to load audio model: {str(e)}")

pipe = load_audio_model()

def generate_audio(prompt: str):
    try:
        audio = pipe(prompt)
        buffer = io.BytesIO()
        buffer.write(audio["audio"].tobytes())
        audio_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return {"audio_base64": audio_b64, "sampling_rate": audio["sampling_rate"]}
    except Exception as e:
        return {"error": f"Audio generation failed: {str(e)}"}

def health_check():
    try:
        _ = pipe("test")
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}