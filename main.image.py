import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from diffusers import DiffusionPipeline
import torch
from PIL import Image
import io
import base64

app = FastAPI()

# Load models on startup
device = "cpu" # Change to "cuda" when using GPU base
models = {}

@app.on_event("startup")
async def load_models():
    try:
        models["sd3.5"] = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-3.5-large", torch_dtype=torch.float16).to(device)
    except Exception as e:
        print(f"Model load error: {e}")

class GenerateRequest(BaseModel):
    model: str  # "sd3.5"
    prompt: str
    num_inference_steps: int = 20
    width: int = 1024
    height: int = 1024

@app.post("/generate")
async def generate_image(req: GenerateRequest):
    if req.model not in models:
        raise HTTPException(status_code=400, detail="Invalid model")
    pipe = models[req.model]
    image = pipe(req.prompt, num_inference_steps=req.num_inference_steps, width=req.width, height=req.height).images[0]
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return {"image_b64": img_str}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)