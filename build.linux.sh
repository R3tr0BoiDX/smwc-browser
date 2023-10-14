#!/bin/bash

# Create a virtual environment
echo "Creating a virtual environment..."
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt -r requirements-dev.txt

# Build the project
echo "Building the project..."
pyinstaller smwc-browser.spec
