FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime

WORKDIR /app
COPY requirements.txt .
COPY app/ app/
COPY main.py .

# Install minimal dependencies in one layer, clean up immediately
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential python3-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && python -c "import diffusers; print('diffusers installed successfully')" \
    && apt-get purge -y build-essential python3-dev \
    && apt-get autoremove -y --purge \
    && rm -rf /var/lib/apt/lists/* /root/.cache /tmp/*

ENV PYTHONUNBUFFERED=1 \
    CUDA_DEVICE_ORDER=PCI_BUS_ID \
    HUGGINGFACE_HUB_CACHE=/dev/shm/hf_cache \
    TRANSFORMERS_CACHE=/dev/shm/transformers_cache

RUN useradd -m appuser && chown -R appuser /app
USER appuser

CMD ["python", "-u", "main.py"]