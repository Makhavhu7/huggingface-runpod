import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import torch
import cv2
import io
import base64

app = FastAPI()

device = "cpu" # Change to "cuda" for GPU
pipe = None

@app.on_event("startup")
async def load_model():
    global pipe
    try:
        pipe = pipeline(Tasks.text_to_video, model="Wan-AI/Wan2.1-T2V-14B", model_revision="v1.1.1")
    except Exception as e:
        print(f"Model load error: {e}")

class GenerateRequest(BaseModel):
    prompt: str
    num_inference_steps: int = 50

@app.post("/generate")
async def generate_video(req: GenerateRequest):
    if pipe is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    try:
        output = pipe({"text": req.prompt, "num_inference_steps": req.num_inference_steps})
        frame = output["videos"][0][0]  # Placeholder for first frame
        ret, buffer = cv2.imencode('.png', frame)
        img_str = base64.b64encode(buffer).decode()
        return {"video_frame_b64": img_str}  # Extend for full video
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)