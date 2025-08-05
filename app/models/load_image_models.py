from diffusers import StableDiffusionXLPipeline
import torch

device = "cuda"

# Load models once and keep warm with FP16 for VRAM savings
sdxl_pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16
).to(device)

flux_pipe = StableDiffusionXLPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev", torch_dtype=torch.float16
).to(device)

def generate_with_sdxl(prompt: str):
    image = sdxl_pipe(prompt).images[0]
    image.save("output_sdxl.png")

def generate_with_flux(prompt: str):
    image = flux_pipe(prompt).images[0]
    image.save("output_flux.png")