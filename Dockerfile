# Build stage
FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime AS builder

WORKDIR /app

# Install dependencies inline, no external file
RUN pip install --no-cache-dir --prefer-binary --no-deps \
    torch>=2.0.0 \
    diffusers>=0.20.0 \
    transformers>=4.30.0

# Copy only the application code
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

# Copy only runtime essentials
COPY --from=builder /app /app

# Environment to minimize disk use
ENV PYTHONUNBUFFERED=1
ENV CUDA_DEVICE_ORDER=PCI_BUS_ID
ENV HUGGINGFACE_HUB_CACHE=/dev/shm/hf_cache
ENV TRANSFORMERS_CACHE=/dev/shm/transformers_cache

CMD ["python", "-u", "main.py"]