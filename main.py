import base64
import asyncio
import json
from app.workers.image_worker import start_image_workers
from app.workers.audio_worker import start_audio_workers
from app.workers.video_worker import start_video_workers
from app.queue_manager import image_queue, audio_queue, video_queue

async def start_all_workers():
    await asyncio.gather(
        start_image_workers(),
        start_audio_workers(),
        start_video_workers()
    )

async def process_image_task(prompt, model, queue):
    queue.put_nowait({"prompt": prompt, "model": model})
    await asyncio.sleep(10)  # Placeholder; replace with callback
    output_file = "output_sdxl.png" if model == "sdxl" else "output_flux.png"
    with open(output_file, "rb") as f:
        img_data = base64.b64encode(f.read()).decode("utf-8")
    return {"status": "Image generated", "prompt": prompt, "model": model, "image": img_data}

def handler(event):
    try:
        input_data = event.get("input", {})
        prompt = input_data.get("prompt", "")
        model = input_data.get("model", "sdxl")

        if not prompt:
            return {"error": "Prompt is required"}

        loop = asyncio.get_event_loop()
        if model in ["sdxl", "flux"]:
            result = loop.run_until_complete(process_image_task(prompt, model, image_queue))
            return result
        elif model == "suno":
            audio_queue.put_nowait({"prompt": prompt, "model": model})
            return {"status": "Audio generation queued", "prompt": prompt, "model": model}
        elif model == "video":
            video_queue.put_nowait({"prompt": prompt})
            return {"status": "Video generation queued", "prompt": prompt}
        else:
            return {"error": "Invalid model specified"}

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_all_workers())