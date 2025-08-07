FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime

WORKDIR /app
COPY requirements.txt .
COPY app/ app/
COPY main.py .

# Install system dependencies for diffusers
RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends \
       build-essential python3-dev libpng-dev libjpeg-dev libopenexr-dev \
       libtiff-dev libwebp-dev cmake libgcc1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && python -c "import diffusers; print('diffusers installed successfully')"

# Clean up system packages
RUN apt-get purge -y build-essential python3-dev cmake \
    && apt-get autoremove -y -qq \
    && rm -rf /root/.cache /tmp/*

ENV PYTHONUNBUFFERED=1 \
    CUDA_DEVICE_ORDER=PCI_BUS_ID \
    HUGGINGFACE_HUB_CACHE=/dev/shm/hf_cache \
    TRANSFORMERS_CACHE=/dev/shm/transformers_cache

RUN useradd -m appuser && chown -R appuser /app
USER appuser

CMD ["python", "-u", "main.py"]