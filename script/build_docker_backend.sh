#!/bin/bash
# This script builds the Docker image for the backend service.

sudo docker build \
	-t backend-service:latest \
	-f docker/backend/Dockerfile \
	.
