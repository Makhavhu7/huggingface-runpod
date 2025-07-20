from diffusers import StableDiffusionPipeline
import torch
import base64
from io import BytesIO

pipe = StableDiffusionPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
).to("cuda" if torch.cuda.is_available() else "cpu")

def generate_image(prompt: str):
    image = pipe(prompt).images[0]
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return {"image_base64": img_b64}