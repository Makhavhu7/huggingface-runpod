FROM nvidia/cuda:12.2.0-devel-ubuntu22.04

WORKDIR /app

# Install Python and pip
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip3 install --no-cache-dir \
    torch==2.1.0 \
    transformers==4.36.2 \
    diffusers==0.21.4 \
    fastapi==0.103.0 \
    uvicorn==0.23.2 \
    scipy==1.11.3

# Copy application files
COPY Image.py .
COPY Video.py .
COPY Audio.py .
COPY server.py .

# Expose port for FastAPI
EXPOSE 8000

# Set environment variable for Hugging Face token (optional, set at runtime)
ENV HF_TOKEN=""

# Run the FastAPI server
CMD ["uvicorn", "server.py:app", "--host", "0.0.0.0", "--port", "8000"]