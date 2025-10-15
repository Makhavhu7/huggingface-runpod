import os
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from modelscope.pipelines import pipeline
import torch
import cv2
import io
import base64

app = FastAPI()

pipe = None

@app.on_event("startup")
async def load_model():
    global pipe
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"🚀 Loading model attempt {attempt + 1}/{max_retries}")
            pipe = pipeline(
                "text-to-video-synthesis", 
                model="Wan-AI/Wan2.2-TI2V-5B", 
                model_revision="bf16",
                cache_dir="/app/model_cache"
            )
            print("✅ Model loaded successfully!")
            return
        except Exception as e:
            print(f"❌ Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)  # Wait 5s before retry
            else:
                print("💥 All retries failed")

class GenerateRequest(BaseModel):
    prompt: str
    num_inference_steps: int = 25

@app.post("/generate")
async def generate_video(req: GenerateRequest):
    if pipe is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    try:
        print(f"🎬 Generating: {req.prompt}")
        output = pipe({"text": req.prompt, "num_inference_steps": req.num_inference_steps})
        frame = output["videos"][0][0]
        ret, buffer = cv2.imencode('.png', frame)
        img_str = base64.b64encode(buffer).decode()
        return {"video_frame_b64": img_str}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)