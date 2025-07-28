#!/bin/bash

# Update system
sudo apt-get update -y
sudo apt-get upgrade -y

# Install Docker
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone your repository (replace with your actual repo)
git clone https://github.com/yourusername/liontech-lms.git
cd liontech-lms

# Create .env file with your configuration
cat > .env <<EOL
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://username:password@your-rds-endpoint:5432/liontech_lms
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=liontechacademy@gmail.com
MAIL_PASSWORD=Dan8080!@#$%
MAIL_DEFAULT_SENDER=liontechacademy@gmail.com
EOL

# Build and run Docker container
sudo docker-compose up --build -d