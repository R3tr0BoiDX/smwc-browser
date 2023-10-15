#!/bin/bash

# May need to install apt install python3-venv

# Remove previous build
echo "Removing previous build..."
rm -rf dist/

# Create a virtual environment
echo "Creating a virtual environment..."
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt -r requirements-dev.txt

# Build the project
echo "Building the project..."
pyinstaller smwc-browser.spec

# Copy the config file
echo "Copying the config file..."
cp config.example.json dist/

# Copy the media folder
echo "Copying the media folder..."
cp -r media dist/

# Zipping the dist folder
echo "Zipping the dist folder..."
zip -r dist/smwc-browser.linux.amd64.zip dist/
