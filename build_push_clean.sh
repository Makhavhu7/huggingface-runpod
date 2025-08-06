#!/bin/bash

# Define image details
IMAGE_NAME="makhavhu/huggingface-runpod"
TAG="latest"

# Debug: Print the combined tag
echo "Building image: $IMAGE_NAME:$TAG"

# Build the image (remove --load for now and test basic build)
docker build -t "$IMAGE_NAME:$TAG" .

# Check if build succeeded
if [ $? -eq 0 ]; then
    echo "Build successful, pushing to Docker Hub..."
    docker push "$IMAGE_NAME:$TAG"
    
    # Check if push succeeded
    if [ $? -eq 0 ]; then
        echo "Push successful, cleaning up..."
        docker rmi "$IMAGE_NAME:$TAG"
        docker builder prune -f
    else
        echo "Push failed, skipping cleanup."
    fi
else
    echo "Build failed."
fi