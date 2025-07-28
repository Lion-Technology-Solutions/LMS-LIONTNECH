#!/bin/bash

# Update system
sudo apt-get update -y
sudo apt-get upgrade -y

# Install Docker
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone your repository (replace with your actual repo)
git clone https://github.com/Lion-Technology-Solutions/LMS-LIONTNECH.git
cd   LMS-LIONTNECH

# Build and run Docker containers
sudo docker-compose up --build -d