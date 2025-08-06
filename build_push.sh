#!/bin/bash
IMAGE_NAME="yourusername/yourapp"
TAG="latest"

# Build with cleanup
docker build --no-cache -t $IMAGE_NAME:$TAG .

# Push to Docker Hub
docker push $IMAGE_NAME:$TAG

# Remove local image and dangling layers
docker rmi $IMAGE_NAME:$TAG
docker system prune -f

echo "Build complete. Image pushed to Docker Hub and local storage cleared."