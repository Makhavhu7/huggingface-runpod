# Stage 1: Build environment
FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime AS builder

WORKDIR /app

# Install minimal dependencies without caching
COPY requirements.txt .
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

# Copy only essential code
COPY app/queue_manager.py app/
COPY app/models/load_image_models.py app/models/
COPY app/models/load_audio_models.py app/models/
COPY app/models/load_video_model.py app/models/
COPY app/workers/audio_worker.py app/workers/
COPY app/workers/image_worker.py app/workers/
COPY app/workers/video_worker.py app/workers/
COPY main.py .

# Stage 2: Runtime environment
FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime

WORKDIR /app

# Copy built dependencies and code
COPY --from=builder /app /app

# Environment settings to minimize storage
ENV PYTHONUNBUFFERED=1
ENV CUDA_DEVICE_ORDER=PCI_BUS_ID
ENV HUGGINGFACE_HUB_CACHE=/dev/shm/hf_cache 
# Use RAM-based tmpfs to avoid disk
ENV TRANSFORMERS_CACHE=/dev/shm/transformers_cache

# Run command
CMD ["python", "-u", "main.py"]