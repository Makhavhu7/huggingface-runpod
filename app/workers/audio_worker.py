import asyncio
from app.queue_manager import audio_queue
from app.models.load_audio_models import generate_audio

async def audio_worker():
    while True:
        task = await audio_queue.get()
        prompt = task.get("prompt", "")
        model = task.get("model", "suno")

        generate_audio(prompt, model)
        print(f"[AUDIO DONE] {model} -> {prompt}")

        audio_queue.task_done()

async def start_audio_workers():
    for _ in range(2):  # Adjust based on GPU load
        asyncio.create_task(audio_worker())