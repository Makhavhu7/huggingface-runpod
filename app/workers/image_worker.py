# backend/app/workers/image_worker.py

import asyncio
from app.queue_manager import image_queue
from app.models.load_image_models import generate_with_flux, generate_with_sdxl

async def image_worker():
    while True:
        task = await image_queue.get()
        prompt = task.get("prompt", "")
        model = task.get("model", "sdxl")

        if model == "flux":
            generate_with_flux(prompt)
        else:
            generate_with_sdxl(prompt)

        print(f"[IMAGE DONE] {model} -> {prompt}")
        image_queue.task_done()

async def start_image_workers():
    for _ in range(2):  # Number of concurrent image workers (tweak for GPU load)
        asyncio.create_task(image_worker())
