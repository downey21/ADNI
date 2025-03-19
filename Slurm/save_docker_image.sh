#!/bin/bash

# Configuration
DOCKER_IMAGE="docker.io/downey21/repo_private:adni_v1"
IMAGE_TAR="/home/dhseo/Images/adni_v1.tar"

# Save Docker image
if [[ ! -f "$IMAGE_TAR" ]]; then
    echo "Saving Docker image to $IMAGE_TAR..."
    docker save -o "$IMAGE_TAR" "$DOCKER_IMAGE"
else
    echo "Docker image tar already exists: $IMAGE_TAR"
fi
