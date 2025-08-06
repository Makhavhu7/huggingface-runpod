#!/bin/bash

# Define image details
IMAGE_NAME="makhavhu/my-ai-app"
TAG="latest"

# Ensure Docker Buildx is set up
docker buildx create --use || true  # Create or use existing builder

# Debug: Print the combined tag
echo "Building and pushing image: $IMAGE_NAME:$TAG"

# Build and push directly to Docker Hub with no local storage
docker buildx build --platform linux/amd64 -t "$IMAGE_NAME:$TAG" . --push

# Check if build and push succeeded
if [ $? -eq 0 ]; then
    echo "Build and push successful, cleaning up local cache..."
    docker builder prune -f
    echo "Local cleanup completed."
else
    echo "Build or push failed. Please check the Dockerfile, network connection, and build logs."
fi