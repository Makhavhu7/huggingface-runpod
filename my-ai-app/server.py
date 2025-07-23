from fastapi import FastAPI, HTTPException
from Image import ImageGenerator
from Video import VideoGenerator
from Audio import AudioGenerator
import os

app = FastAPI()

# Initialize generators
image_gen = ImageGenerator()
video_gen = VideoGenerator()
audio_gen = AudioGenerator()

@app.get("/health")
async def health_check():
    return {
        "image_model": image_gen.health_check(),
        "video_model": video_gen.health_check(),
        "audio_model": audio_gen.health_check()
    }

@app.post("/generate/image")
async def generate_image(prompt: str):
    try:
        output_path = image_gen.generate(prompt)
        return {"output": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/video")
async def generate_video(prompt: str):
    try:
        output_path = video_gen.generate(prompt)
        return {"output": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/audio")
async def generate_audio(prompt: str):
    try:
        output_path = audio_gen.generate(prompt)
        return {"output": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))