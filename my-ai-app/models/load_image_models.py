# backend/app/models/load_image_models.py

from diffusers import StableDiffusionXLPipeline
import touch

device = "cuda"

# Load models once and keep warm
sdxl_pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0"
).to(device)

flux_pipe = StableDiffusionXLPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev"
).to(device)

def generate_with_sdxl(prompt: str):
    image = sdxl_pipe(prompt).images[0]
    image.save("output_sdxl.png")

def generate_with_flux(prompt: str):
    image = flux_pipe(prompt).images[0]
    image.save("output_flux.png")
