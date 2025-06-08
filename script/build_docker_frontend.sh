#!/bin/bash
# This script builds the Docker image for the backend service.

# move dependice from pyproject to requirements.txt

sudo docker build \
	-t frontend-service:latest \
	-f docker/frontend/Dockerfile \
	.
