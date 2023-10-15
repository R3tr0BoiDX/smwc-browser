# May need to run in order be be able to execute:
# Set-ExecutionPolicy RemoteSigned

# Remove previous build
Write-Host "Removing previous build..."
Remove-Item -Path ".\build" -Recurse -Force

# Create a virtual environment
Write-Host "Creating a virtual environment..."
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt

# Build the project
Write-Host "Building the project..."
python .\setup.py build

# Get the build folder
Write-Host "Getting the build folder..."
$buildFolder = Get-ChildItem -Path ".\build\exe.win-amd64*" -Directory | Select-Object -First 1

# Copy the config file
Write-Host "Copying the config file..."
Copy-Item .\config.example.json $buildFolder\config.example.json

# Copy the media folder
Write-Host "Copying the media folder..."
Copy-Item .\media $buildFolder\media -Recurse

# Zipping the build folder
Write-Host "Zipping the build folder..."
Get-ChildItem -Path $buildFolder\* | Compress-Archive -DestinationPath ".\build\smwc-browser.windows.amd64.zip"