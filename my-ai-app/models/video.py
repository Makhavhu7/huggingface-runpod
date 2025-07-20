from diffusers import DiffusionPipeline
import torch
import base64
import imageio

pipe = DiffusionPipeline.from_pretrained(
    "Wan-AI/Wan2.1-T2V-14B",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
).to("cuda" if torch.cuda.is_available() else "cpu")

def generate_video(prompt: str):
    video_frames = pipe(prompt, num_frames=16).frames
    writer = imageio.get_writer("video.mp4", fps=8)
    for frame in video_frames:
        writer.append_data(frame)
    writer.close()
    with open("video.mp4", "rb") as f:
        video_b64 = base64.b64encode(f.read()).decode("utf-8")
    return {"video_base64": video_b64}