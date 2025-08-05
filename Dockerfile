# Use a slimmer base image with PyTorch and CUDA
FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime

WORKDIR /app

# Install dependencies in one layer to reduce image size
RUN pip install --no-cache-dir --prefer-binary \
    torch==2.0.0 \
    diffusers==0.20.0 \
    transformers==4.30.0

# Copy only necessary application code
COPY app/queue_manager.py app/
COPY app/models/load_image_models.py app/models/
COPY app/models/load_audio_models.py app/models/
COPY app/models/load_video_model.py app/models/
COPY app/workers/audio_worker.py app/workers/
COPY app/workers/image_worker.py app/workers/
COPY app/workers/video_worker.py app/workers/
COPY main.py .

# Environment variables for optimization
ENV PYTHONUNBUFFERED=1 \
    CUDA_DEVICE_ORDER=PCI_BUS_ID \
    HUGGINGFACE_HUB_CACHE=/dev/shm/hf_cache \
    TRANSFORMERS_CACHE=/dev/shm/transformers_cache

# Use non-root user for security
RUN useradd -m appuser && chown -R appuser /app
USER appuser

CMD ["python", "-u", "main.py"]