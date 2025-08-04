import asyncio
from app.queue_manager import video_queue
from app.models.load_video_model import generate_video

async def video_worker():
    while True:
        task = await video_queue.get()
        prompt = task.get("prompt", "")
        generate_video(prompt)
        print(f"[VIDEO DONE] {prompt}")
        video_queue.task_done()

async def start_video_workers():
    for _ in range(1):  # Most video models are VRAM heavy
        asyncio.create_task(video_worker())
