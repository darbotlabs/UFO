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
