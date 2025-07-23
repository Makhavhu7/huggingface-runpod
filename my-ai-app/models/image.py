from diffusers import StableDiffusionPipeline
import torch
import os

class ImageGenerator:
    def __init__(self):
        model_id = "stabilityai/stable-diffusion-3.5-large"
        self.pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
            use_auth_token=os.getenv("HF_TOKEN", None)
        )
        self.pipe = self.pipe.to("cuda" if torch.cuda.is_available() else "cpu")

    def generate(self, prompt, output_path="output_image.png"):
        image = self.pipe(prompt, num_inference_steps=50, guidance_scale=7.5).images[0]
        image.save(output_path)
        return output_path

    def health_check(self):
        return self.pipe is not None