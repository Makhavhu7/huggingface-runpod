from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import image
import video
import audio

app = FastAPI()

class Prompt(BaseModel):
    prompt: str

@app.post("/generate/image")
async def generate_image_endpoint(request: Prompt):
    try:
        result = image.generate_image(request.prompt)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")

@app.post("/generate/video")
async def generate_video_endpoint(request: Prompt):
    try:
        result = video.generate_video(request.prompt)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Video generation failed: {str(e)}")

@app.post("/generate/audio")
async def generate_audio_endpoint(request: Prompt):
    try:
        result = audio.generate_audio(request.prompt)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio generation failed: {str(e)}")

@app.get("/health/image")
async def image_health():
    return image.health_check()

@app.get("/health/video")
async def video_health():
    return video.health_check()

@app.get("/health/audio")
async def audio_health():
    return audio.health_check()