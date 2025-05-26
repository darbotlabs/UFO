# Create a dedicated DARBOT folder for organizing all UFO² installation and validation files
# Created: May 25, 2025

# Create the darbot directory if it doesn't exist
Write-Host "Creating DARBOT directory..." -ForegroundColor Cyan
New-Item -Path "g:\Github\UFO\darbot" -ItemType Directory -Force | Out-Null

# List of files to copy to the darbot directory
$filesToCopy = @(
    "install_ufo_dependencies.ps1",
    "quick_check.py",
    "comprehensive_validation.py",
    "test_api_connectivity.py",
    "fix_azure_config.py",
    "test_mission.py",
    "updated_mission_pack.md",
    "mission_report_2025-05-01.md",
    "FullStepsandTroubleshooting.md"
)

# Copy README to darbot folder
Write-Host "Copying DARBOT README..." -ForegroundColor Cyan
Copy-Item -Path "g:\Github\UFO\DARBOT_README.md" -Destination "g:\Github\UFO\darbot\README.md" -Force

# Copy each file to the darbot directory
foreach ($file in $filesToCopy) {
    $sourcePath = "g:\Github\UFO\$file"
    $destPath = "g:\Github\UFO\darbot\$file"
    
    if (Test-Path -Path $sourcePath) {
        Write-Host "Copying $file to darbot folder..." -ForegroundColor Green
        Copy-Item -Path $sourcePath -Destination $destPath -Force
    }
    else {
        Write-Host "Warning: $file not found in source directory" -ForegroundColor Yellow
    }
}

# Copy requirements.txt if exists
if (Test-Path -Path "g:\Github\UFO\requirements.txt") {
    Write-Host "Copying requirements.txt to darbot folder..." -ForegroundColor Green
    Copy-Item -Path "g:\Github\UFO\requirements.txt" -Destination "g:\Github\UFO\darbot\requirements.txt" -Force
}

# Check if environment variables script exists and copy it
$envVarsPath = "g:\Github\UFO\set_ufo_env_vars.ps1"
if (Test-Path -Path $envVarsPath) {
    Write-Host "Copying environment variables script to darbot folder..." -ForegroundColor Green
    Copy-Item -Path $envVarsPath -Destination "g:\Github\UFO\darbot\set_ufo_env_vars.ps1" -Force
}
else {
    # Create a template environment variables script if it doesn't exist
    Write-Host "Creating environment variables template script in darbot folder..." -ForegroundColor Yellow
    @'
# UFO² Environment Variables Setup
# Run this script to set environment variables for your API keys

# Azure OpenAI Variables
$env:AZURE_OPENAI_API_KEY = "your-api-key-here"
$env:AZURE_OPENAI_ENDPOINT = "https://your-resource-name.openai.azure.com"
$env:AZURE_OPENAI_DEPLOYMENT = "your-deployment-name"

# OpenAI Variables
$env:OPENAI_API_KEY = "your-api-key-here"

# To make these variables persistent across sessions:
# 1. In PowerShell, run:
#    [System.Environment]::SetEnvironmentVariable("AZURE_OPENAI_API_KEY", "your-api-key-here", "User")
#    [System.Environment]::SetEnvironmentVariable("AZURE_OPENAI_ENDPOINT", "https://your-resource-name.openai.azure.com", "User")
#    [System.Environment]::SetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT", "your-deployment-name", "User")
#    [System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "your-api-key-here", "User")
#
# 2. Then update config.yaml to reference these variables:
#    API_KEY: "${AZURE_OPENAI_API_KEY}"
#    API_BASE: "${AZURE_OPENAI_ENDPOINT}"
#    API_DEPLOYMENT_ID: "${AZURE_OPENAI_DEPLOYMENT}"
'@ | Out-File -FilePath "g:\Github\UFO\darbot\set_ufo_env_vars.ps1" -Encoding utf8
}

# Create a completion message
Write-Host "`nDARBOT files have been organized into g:\Github\UFO\darbot\" -ForegroundColor Magenta
Write-Host "You can now run the installation and validation scripts from this folder" -ForegroundColor Magenta
Write-Host "`nTo get started:" -ForegroundColor Cyan
Write-Host "1. cd g:\Github\UFO\darbot" -ForegroundColor White
Write-Host "2. .\install_ufo_dependencies.ps1" -ForegroundColor White
Write-Host "`nRefer to the README.md file for complete documentation" -ForegroundColor Cyan
