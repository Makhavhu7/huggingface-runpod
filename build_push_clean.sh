#!/bin/bash
IMAGE_NAME="makhavhu/huggingface-runpod:latest"
TAG="latest"

# Build with platform specification (adjust if needed)
docker buildx build --platform linux/amd64 -t $IMAGE_NAME:$TAG . --load

# Push to Docker Hub
docker push $IMAGE_NAME:$TAG

# Remove local image and build cache
docker rmi $IMAGE_NAME:$TAG
docker builder prune -f