import asyncio
import base64
import json
from app.workers.image_worker import start_image_workers
from app.workers.audio_worker import start_audio_workers
from app.workers.video_worker import start_video_workers
from app.queue_manager import image_queue, audio_queue, video_queue

async def start_all_workers():
    """Start all worker processes concurrently."""
    await asyncio.gather(
        start_image_workers(),
        start_audio_workers(),
        start_video_workers()
    )

async def process_image_task(prompt: str, model: str, queue):
    """Process an image generation task."""
    queue.put_nowait({"prompt": prompt, "model": model})
    await asyncio.sleep(10)  # Simulate processing delay
    output_file = f"output_{model}.png"
    try:
        with open(output_file, "rb") as f:
            img_data = base64.b64encode(f.read()).decode("utf-8")
        return {"status": "Image generated", "prompt": prompt, "model": model, "image": img_data}
    except FileNotFoundError:
        return {"error": f"Output file {output_file} not found"}

def handler(event: dict) -> dict:
    """Handle incoming events and route to appropriate task."""
    try:
        input_data = event.get("input", {})
        prompt = input_data.get("prompt", "")
        model = input_data.get("model", "sdxl")

        if not prompt:
            return {"error": "Prompt is required"}

        loop = asyncio.get_event_loop()
        if model in ["sdxl", "flux"]:
            return loop.run_until_complete(process_image_task(prompt, model, image_queue))
        elif model == "suno":
            audio_queue.put_nowait({"prompt": prompt, "model": model})
            return {"status": "Audio generation queued", "prompt": prompt, "model": model}
        elif model == "video":
            video_queue.put_nowait({"prompt": prompt})
            return {"status": "Video generation queued", "prompt": prompt}
        else:
            return {"error": f"Invalid model: {model}"}

    except Exception as e:
        return {"error": f"Handler error: {str(e)}"}

if __name__ == "__main__":
    try:
        asyncio.run(start_all_workers())
    except Exception as e:
        print(f"Error starting workers: {str(e)}")