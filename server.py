from fastapi import FastAPI, Request
from models.image import generate_image
from models.audio import generate_audio
from models.video import generate_video

app = FastAPI()

@app.post("/generate-image")
async def image_endpoint(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    return generate_image(prompt)

@app.post("/generate-audio")
async def audio_endpoint(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    return generate_audio(prompt)

@app.post("/generate-video")
async def video_endpoint(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    return generate_video(prompt)

