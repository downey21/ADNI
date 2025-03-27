#!/bin/bash
#SBATCH --job-name=sbatch_dicom_to_nifti_parallel_example_python
#SBATCH --partition=cpu
#SBATCH --nodelist=node01
#SBATCH --cpus-per-task=20
#SBATCH --mem=0
#SBATCH --time=3-23:59:59
#SBATCH --output=output_sbatch_dicom_to_nifti_parallel_example_python.log
#SBATCH --error=output_sbatch_dicom_to_nifti_parallel_example_python.log

# sudo sbatch sbatch_dicom_to_nifti_parallel_example_python.sh

# Configuration
DOCKER_IMAGE="docker.io/downey21/repo_private:adni_v1"
IMAGE_TAR="/home/dhseo/Images/adni_v1.tar"

# Check if Docker image tar exists
if [[ ! -f "$IMAGE_TAR" ]]; then
    echo "Error: Docker image tar file not found: $IMAGE_TAR"
    exit 1
fi

# Forcefully remove the existing image and reload a new one
EXISTING_IMAGE_ID=$(docker images | grep "$(basename "$DOCKER_IMAGE" | cut -d':' -f1)" | awk '{print $3}')
if [[ -n "$EXISTING_IMAGE_ID" ]]; then
    echo "Removing old Docker image: $EXISTING_IMAGE_ID"
    docker rmi -f "$EXISTING_IMAGE_ID"
fi

echo "Loading Docker image from $IMAGE_TAR..."
docker load -i "$IMAGE_TAR"

# Run the container
echo "Running the DICOM to NIfTI conversion..."
docker run --rm \
    -v /node05_storage:/root/data \
    -v /home/dhseo/Project:/root/Project \
    "$DOCKER_IMAGE" \
    env PYTHONDONTWRITEBYTECODE=1 python3 /root/Project/ADNI/Python/dicom_to_nifti_parallel.py

# Check Docker run success
if [[ $? -ne 0 ]]; then
    echo "Error: Docker execution failed"
    exit 1
else
    echo "DICOM to NIfTI conversion completed successfully!"
fi
