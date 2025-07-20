FROM python:3.10-slim

WORKDIR /app

# Install minimal system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg libsndfile1 git curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy and install only required Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    pydub \
    && pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir transformers diffusers accelerate \
    && pip install --no-cache-dir git+https://github.com/suno-ai/bark.git

# Copy the rest of the application
COPY . .

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]