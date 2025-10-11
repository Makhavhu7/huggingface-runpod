import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from diffusers import DiffusionPipeline
import torch
from PIL import Image
import io
import base64

app = FastAPI()

# Load models on startup (use /dev/shm cache)
device = "cuda" if torch.cuda.is_available() else "cpu"
models = {}

@app.on_event("startup")
async def load_models():
    try:
        models["sdxl"] = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16).to(device)
        models["flux"] = DiffusionPipeline.from_pretrained("black-forest-labs/FLUX.1-dev", torch_dtype=torch.float16).to(device)
    except Exception as e:
        print(f"Model load error: {e}")

class GenerateRequest(BaseModel):
    model: str  # "sdxl" or "flux"
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
    # Encode to base64 for API response
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return {"image_b64": img_str}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)