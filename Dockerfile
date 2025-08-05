# Build stage
FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime AS builder

WORKDIR /app

# Install only what’s needed, no extras
COPY requirements.txt .
RUN pip install --no-cache-dir --prefer-binary --no-deps -r requirements.txt

# Copy just the code
COPY app/queue_manager.py app/
COPY app/models/load_image_models.py app/models/
COPY app/models/load_audio_models.py app/models/
COPY app/models/load_video_model.py app/models/
COPY app/workers/audio_worker.py app/workers/
COPY app/workers/image_worker.py app/workers/
COPY app/workers/video_worker.py app/workers/
COPY main.py .

# Runtime stage
FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime

WORKDIR /app

COPY --from=builder /app /app

# Use RAM for caches, skip disk
ENV PYTHONUNBUFFERED=1
ENV CUDA_DEVICE_ORDER=PCI_BUS_ID
ENV HUGGINGFACE_HUB_CACHE=/dev/shm/hf_cache
ENV TRANSFORMERS_CACHE=/dev/shm/transformers_cache

CMD ["python", "-u", "main.py"]