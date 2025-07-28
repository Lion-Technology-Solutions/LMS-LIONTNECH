#!/bin/bash

# Wait for the database to be ready
while ! nc -z db 5432; do
  sleep 0.1
done

# Initialize the database
flask shell <<EOF
from app import db
db.create_all()
exit()
EOF

# Run the application
gunicorn --bind 0.0.0.0:5000 run:app