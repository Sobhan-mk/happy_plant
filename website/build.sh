#!/usr/bin/env bash

echo "Downloading model file..."
# Replace FILE_ID with your actual Google Drive file ID
gdown https://drive.google.com/uc?id=1wLw-mr1Y-mQBk6AQc3ooWnxMVCf3v1kd -O house_plant_species_detector.pth

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running database migrations..."
python manage.py migrate
