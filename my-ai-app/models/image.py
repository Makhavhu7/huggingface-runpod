import torch
from diffusers import StableDiffusionPipeline
import base64
from io import BytesIO

def load_image_model():
    try:
        pipe = StableDiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-3.5-large",
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            use_auth_token=True
        ).to("cuda" if torch.cuda.is_available() else "cpu")
        return pipe
    except Exception as e:
        raise Exception(f"Failed to load image model: {str(e)}")

pipe = load_image_model()

def generate_image(prompt: str):
    try:
        image = pipe(prompt).images[0]
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return {"image_base64": img_b64}
    except Exception as e:
        return {"error": f"Image generation failed: {str(e)}"}

def health_check():
    try:
        _ = pipe("test prompt", num_inference_steps=1)
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}