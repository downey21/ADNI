#!/bin/bash
#SBATCH --job-name=sbatch_preprocessing_fMRI_parallel_example_python
#SBATCH --partition=cpu
#SBATCH --nodelist=node01
#SBATCH --cpus-per-task=10
#SBATCH --mem=0
#SBATCH --time=3-23:59:59
#SBATCH --output=sbatch_preprocessing_fMRI_parallel_example_python.log
#SBATCH --error=sbatch_preprocessing_fMRI_parallel_example_python.log

# sudo sbatch sbatch_preprocessing_fMRI_parallel_example_python.sh

# Configuration
DOCKER_IMAGE="docker.io/downey21/repo_private:adni_v1"
IMAGE_TAR="/home/dhseo/Images/adni_v1.tar"

# Check if Docker image tar exists
if [[ ! -f "$IMAGE_TAR" ]]; then
    echo "Error: Docker image tar file not found: $IMAGE_TAR"
    exit 1
fi

# Check if image is already loaded
if ! docker images | grep -q "$(basename "$DOCKER_IMAGE" | cut -d':' -f1)"; then
    echo "Loading Docker image from $IMAGE_TAR..."
    docker load -i "$IMAGE_TAR"
else
    echo "Docker image already loaded, skipping load step."
fi

# Run the container
echo "Running the preprocessing MRI..."
docker run --rm \
    -v /node05_storage:/root/data \
    -v /home/dhseo/Project:/root/Project \
    "$DOCKER_IMAGE" \
    bash -i -c "source ~/.bashrc && env PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 python3 /root/Project/ADNI/Python/preprocessing_fMRI_parallel.py"

# Check Docker run success
if [[ $? -ne 0 ]]; then
    echo "Error: Docker execution failed"
    exit 1
else
    echo "preprocessing MRI completed successfully!"
fi
