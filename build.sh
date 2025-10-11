#!/bin/bash
# For local "Docker Play" testing
docker build -f Dockerfile.image -t my-ai-image:latest .
docker build -f Dockerfile.video -t my-ai-video:latest .
docker build -f Dockerfile.audio -t my-ai-audio:latest .
echo "Builds complete. Run e.g., docker run -p 8000:8000 --gpus all my-ai-image:latest"