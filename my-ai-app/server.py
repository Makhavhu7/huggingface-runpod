from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import image1
import image2
import audio
import video

app = FastAPI()

class Prompt(BaseModel):
    prompt: str

@app.post("/generate/image1")
async def generate_image1_endpoint(request: Prompt):
    try:
        result = image1.generate_image(request.prompt)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image1 generation failed: {str(e)}")

@app.post("/generate/image2")
async def generate_image2_endpoint(request: Prompt):
    try:
        result = image2.generate_image(request.prompt)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image2 generation failed: {str(e)}")

@app.post("/generate/audio")
async def generate_audio_endpoint(request: Prompt):
    try:
        result = audio.generate_audio(request.prompt)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio generation failed: {str(e)}")

@app.post("/generate/video")
async def generate_video_endpoint(request: Prompt):
    try:
        result = video.generate_video(request.prompt)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Video generation failed: {str(e)}")

@app.get("/health/image1")
async def image1_health():
    return image1.health_check()

@app.get("/health/image2")
async def image2_health():
    return image2.health_check()

@app.get("/health/audio")
async def audio_health():
    return audio.health_check()

@app.get("/health/video")
async def video_health():
    return video.health_check()