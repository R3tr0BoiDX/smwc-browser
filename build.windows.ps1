# May need to run in order be be able to execute:
# Set-ExecutionPolicy RemoteSigned

# Create a virtual environment
Write-Host "Creating a virtual environment..."
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt

# Build the project
Write-Host "Building the project..."
pyinstaller smwc-browser.spec --icon=resources\windows_icon.ico

# Copy the config file
Write-Host "Copying the config file..."
Copy-Item .\config.example.json .\dist\config.example.json

# Copy the media folder
Write-Host "Copying the media folder..."
Copy-Item .\media .\dist\media -Recurse

# Zipping the dist folder
Write-Host "Zipping the dist folder..."
Compress-Archive -Path .\dist\ -DestinationPath .\dist\smwc-browser.windows.amd64.zip