# Builder stage
FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime AS builder

WORKDIR /app
COPY app/ app/
COPY main.py .

# Install minimal dependencies and verify installation
RUN pip install --no-cache-dir \
    torch==2.0.0 \
    diffusers==0.20.0 \
    transformers==4.30.0 \
    && python -c "import diffusers; print('diffusers installed successfully')" \
    && find / -name "__pycache__" -exec rm -rf {} + \
    && rm -rf /root/.cache /tmp/*

# Runtime stage
FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime

WORKDIR /app
COPY --from=builder /app /app

ENV PYTHONUNBUFFERED=1 \
    CUDA_DEVICE_ORDER=PCI_BUS_ID \
    HUGGINGFACE_HUB_CACHE=/dev/shm/hf_cache \
    TRANSFORMERS_CACHE=/dev/shm/transformers_cache

RUN useradd -m appuser && chown -R appuser /app
USER appuser

CMD ["python", "-u", "main.py"]