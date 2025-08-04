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

def handler(event):
    """
    RunPod serverless handler function.
    Expects input in the format: {"input": {"prompt": "string", "model": "sdxl|flux|suno|video"}}
    """
    try:
        input_data = event.get("input", {})
        prompt = input_data.get("prompt", "")
        model = input_data.get("model", "sdxl")

        if not prompt:
            return {"error": "Prompt is required"}

        # Enqueue task based on model type
        if model in ["sdxl", "flux"]:
            image_queue.put_nowait({"prompt": prompt, "model": model})
            return {"status": "Image generation queued", "prompt": prompt, "model": model}
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

# Start workers when the container starts
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_all_workers())