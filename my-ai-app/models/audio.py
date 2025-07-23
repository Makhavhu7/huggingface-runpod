import torch
from transformers import pipeline

def load_audio_model():
    try:
        pipe = pipeline(
            "text-to-speech",
            model="suno/bark",
            device="cuda" if torch.cuda.is_available() else "cpu"
        )
        return pipe
    except Exception as e:
        raise Exception(f"Failed to load audio model: {str(e)}")

pipe = load_audio_model()

def generate_audio(prompt: str):
    try:
        audio = pipe(prompt)
        return {"audio": audio}  # Simplified; actual encoding depends on output format
    except Exception as e:
        return {"error": f"Audio generation failed: {str(e)}"}

def health_check():
    try:
        _ = pipe("test")
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}