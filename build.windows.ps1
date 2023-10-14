# May need to run:
# Set-ExecutionPolicy RemoteSigned

# Create a virtual environment
Write-Host "Creating a virtual environment..."
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt

# Build the project
Write-Host "Building the project..."
pyinstaller smwc-browser.spec