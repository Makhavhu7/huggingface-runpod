#!/bin/bash

# Define image details
IMAGE_NAME="makhavhu/my-ai-app"
TAG="latest"

# Ensure Docker Buildx is set up
docker buildx create --use || true

# Debug: Print the combined tag
echo "Building and pushing image: $IMAGE_NAME:$TAG"

# Build and push directly to Docker Hub
docker buildx build --platform linux/amd64 -t "$IMAGE_NAME:$TAG" . --push

# Check if build and push succeeded
if [ $? -eq 0 ]; then
    echo "Build and push successful."
else
    echo "Build or push failed. Please check the Dockerfile, network connection, and build logs."
fi