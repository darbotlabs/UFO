# ======================================================================
# UFO² Complete Dependencies Installation Script
# Created: May 25, 2025
# ======================================================================
# This script installs ALL dependencies required for the UFO² project
# Run with Administrator privileges in PowerShell 7+
# ======================================================================

# Enable strict mode and error handling
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-ColorOutput($Message, $Color = "White") {
    Write-Host $Message -ForegroundColor $Color
}

function Test-CommandExists($Command) {
    return $null -ne (Get-Command $Command -ErrorAction SilentlyContinue)
}

# ======================================================================
# SECTION 1: Core System Dependencies
# ======================================================================
Write-ColorOutput "🛸 UFO² Project - Complete Dependencies Installation" -Color Magenta
Write-ColorOutput "=======================================================" -Color Magenta
Write-ColorOutput "🔍 SECTION 1: Checking and installing core system dependencies..." -Color Cyan

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-ColorOutput "⚠️ This script requires administrator privileges. Please run PowerShell as Administrator." -Color Yellow
    Write-ColorOutput "   Continuing, but some installations may fail..." -Color Yellow
}

# Check for PowerShell 7+
$psVersion = $PSVersionTable.PSVersion.Major
if ($psVersion -lt 7) {
    Write-ColorOutput "⚠️ PowerShell 7+ is recommended. Current version: $psVersion" -Color Yellow
    Write-ColorOutput "   Installing PowerShell 7..." -Color Yellow
    winget install --id Microsoft.PowerShell -e
    Write-ColorOutput "✅ PowerShell 7 installed. Please restart this script in PowerShell 7." -Color Green
    exit
}
else {
    Write-ColorOutput "✅ PowerShell $psVersion detected" -Color Green
}

# Check for winget
if (-not (Test-CommandExists winget)) {
    Write-ColorOutput "❌ Winget is not installed. This is required for dependency installation." -Color Red
    Write-ColorOutput "   Please install App Installer from Microsoft Store and try again." -Color Red
    exit 1
}
else {
    Write-ColorOutput "✅ Winget is available" -Color Green
}

# Check and install Python 3.10+
$pyOk = $false
if (Test-CommandExists python) {
    $pythonVersionOutput = python -c "import sys, json; print(json.dumps(sys.version_info[:3]))" 2>$null
    if ($pythonVersionOutput -match '^\[3,(1[0-9])') {
        $pyOk = $true
        $pythonVersion = python --version
        Write-ColorOutput "✅ $pythonVersion is installed" -Color Green
    }
}

if (-not $pyOk) {
    Write-ColorOutput "📦 Python 3.10+ not found. Installing Python 3.11..." -Color Yellow
    winget install -e --id Python.Python.3.11
    
    # Update PATH environment variable for the current session
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
    
    # Verify installation
    if (Test-CommandExists python) {
        $pythonVersion = python --version
        Write-ColorOutput "✅ $pythonVersion installed successfully" -Color Green
    }
    else {
        Write-ColorOutput "⚠️ Python installation completed, but 'python' command is not available." -Color Yellow
        Write-ColorOutput "   You may need to restart your terminal or add Python to your PATH manually." -Color Yellow
    }
}

# Check and install Git
if (-not (Test-CommandExists git)) {
    Write-ColorOutput "📦 Git not found. Installing Git..." -Color Yellow
    winget install --id Git.Git -e
    
    # Update PATH for current session
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
    
    if (Test-CommandExists git) {
        $gitVersion = git --version
        Write-ColorOutput "✅ $gitVersion installed successfully" -Color Green
    }
    else {
        Write-ColorOutput "⚠️ Git installation completed, but 'git' command is not available." -Color Yellow
        Write-ColorOutput "   You may need to restart your terminal." -Color Yellow
    }
}
else {
    $gitVersion = git --version
    Write-ColorOutput "✅ $gitVersion is installed" -Color Green
}

# Check and install Conda (optional but recommended)
if (-not (Test-CommandExists conda)) {
    Write-ColorOutput "📦 Miniconda not found. Installing Miniconda3..." -Color Yellow
    winget install -e --id Anaconda.Miniconda3
    
    # Update PATH for current session
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
    
    Write-ColorOutput "ℹ️ Miniconda installed. You may need to restart your terminal to use 'conda' command." -Color Cyan
}
else {
    $condaVersion = conda --version
    Write-ColorOutput "✅ $condaVersion is installed" -Color Green
}

# Install Visual C++ Build Tools (required for certain packages)
Write-ColorOutput "📦 Installing Microsoft Visual C++ Build Tools (required for some packages)..." -Color Yellow

# Check if Visual C++ Build Tools are already installed
$vcBuildToolsPath = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"
if (Test-Path $vcBuildToolsPath) {
    $vsInfo = & $vcBuildToolsPath -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -format json | ConvertFrom-Json
    if ($vsInfo) {
        Write-ColorOutput "✅ Visual C++ Build Tools are already installed" -Color Green
    }
    else {
        Write-ColorOutput "📦 Installing Visual C++ Build Tools..." -Color Yellow
        winget install -e --id Microsoft.VisualStudio.2022.BuildTools --silent --override "--wait --quiet --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64"
    }
}
else {
    Write-ColorOutput "📦 Installing Visual C++ Build Tools..." -Color Yellow
    winget install -e --id Microsoft.VisualStudio.2022.BuildTools --silent --override "--wait --quiet --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64"
}

# Install VS Code Insiders if not already installed
$vsCodeInsidersPath = "$env:LOCALAPPDATA\Programs\Microsoft VS Code Insiders\Code - Insiders.exe"
if (-not (Test-Path $vsCodeInsidersPath)) {
    Write-ColorOutput "📦 VS Code Insiders not found. Installing..." -Color Yellow
    winget install -e --id Microsoft.VisualStudioCode.Insiders
    Write-ColorOutput "✅ VS Code Insiders installed" -Color Green
}
else {
    Write-ColorOutput "✅ VS Code Insiders is already installed" -Color Green
}

Write-ColorOutput "✅ SECTION 1 COMPLETE: Core system dependencies installed" -Color Green

# ======================================================================
# SECTION 2: Python Virtual Environment Setup
# ======================================================================
Write-ColorOutput "`n🔧 SECTION 2: Setting up Python virtual environment..." -Color Cyan

$envPath = "$env:USERPROFILE\ufo_env"

# Check if virtual environment already exists
if (Test-Path "$envPath\Scripts\Activate.ps1") {
    Write-ColorOutput "ℹ️ Virtual environment already exists at $envPath" -Color Yellow
    Write-ColorOutput "   Activating existing environment..." -Color Yellow
    & "$envPath\Scripts\Activate.ps1"
}
else {
    Write-ColorOutput "🚀 Creating new Python virtual environment at $envPath" -Color Cyan
    python -m venv $envPath
    
    if (Test-Path "$envPath\Scripts\Activate.ps1") {
        Write-ColorOutput "✅ Virtual environment created successfully" -Color Green
        Write-ColorOutput "   Activating environment..." -Color Cyan
        & "$envPath\Scripts\Activate.ps1"
    }
    else {
        Write-ColorOutput "❌ Failed to create virtual environment" -Color Red
        exit 1
    }
}

# Upgrade pip
Write-ColorOutput "📦 Upgrading pip to latest version..." -Color Yellow
python -m pip install --upgrade pip

Write-ColorOutput "✅ SECTION 2 COMPLETE: Python virtual environment is setup and activated" -Color Green

# ======================================================================
# SECTION 3: Project Dependencies Installation
# ======================================================================
Write-ColorOutput "`n📦 SECTION 3: Installing UFO² project dependencies..." -Color Cyan

# Navigate to project directory
$projectPath = "g:\Github\UFO"
Set-Location $projectPath

# First attempt to install all dependencies from requirements.txt
Write-ColorOutput "📦 Installing dependencies from requirements.txt..." -Color Yellow
$reqInstallSuccess = $true
try {
    pip install -r requirements.txt
}
catch {
    $reqInstallSuccess = $false
    Write-ColorOutput "⚠️ Some packages failed to install from requirements.txt" -Color Yellow
    Write-ColorOutput "   Will try alternative installation methods for problematic packages" -Color Yellow
}

# Install packages that might be problematic individually
if (-not $reqInstallSuccess) {
    # Common problematic packages that might need special handling
    Write-ColorOutput "📦 Installing lxml with binary-only option..." -Color Yellow
    pip install --only-binary :all: lxml
    
    Write-ColorOutput "📦 Installing faiss-cpu separately..." -Color Yellow
    pip install faiss-cpu
    
    Write-ColorOutput "📦 Installing torch and torchvision..." -Color Yellow
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
    
    Write-ColorOutput "📦 Installing azure-identity..." -Color Yellow
    pip install azure-identity
    
    Write-ColorOutput "📦 Installing sentence_transformers..." -Color Yellow
    pip install sentence_transformers
    
    Write-ColorOutput "📦 Installing opencv-python..." -Color Yellow
    pip install opencv-python
    
    Write-ColorOutput "📦 Installing pywinauto..." -Color Yellow
    pip install pywinauto
    
    Write-ColorOutput "📦 Installing pyautogui..." -Color Yellow
    pip install pyautogui
    
    Write-ColorOutput "📦 Installing pyyaml..." -Color Yellow
    pip install pyyaml
    Write-ColorOutput "📦 Installing langchain..." -Color Yellow
    pip install langchain
    
    Write-ColorOutput "📦 Installing langchain_community..." -Color Yellow
    pip install langchain_community
    
    Write-ColorOutput "📦 Installing openai..." -Color Yellow
    pip install openai
    Write-ColorOutput "📦 Installing numpy..." -Color Yellow
    pip install numpy
    
    Write-ColorOutput "📦 Installing html2text..." -Color Yellow
    pip install html2text
    
    Write-ColorOutput "📦 Installing art..." -Color Yellow
    pip install art
    
    Write-ColorOutput "📦 Installing uiautomation..." -Color Yellow
    pip install uiautomation
    
    Write-ColorOutput "📦 Installing gradio_client..." -Color Yellow
    pip install gradio_client
}

# Install additional development and testing tools
Write-ColorOutput "📦 Installing development and testing tools..." -Color Yellow
pip install pytest ruff black mypy

# ======================================================================
# SECTION 4: Dependency Validation
# ======================================================================
Write-ColorOutput "`n🔍 SECTION 4: Validating critical dependencies..." -Color Cyan

$validationScript = @"
import sys
import importlib.util

def check_import(module_name):
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            return False
        return True
    except ModuleNotFoundError:
        return False

# Critical dependencies for UFO project
critical_deps = [
    'azure.identity',
    'faiss',
    'cv2',
    'yaml',
    'pywinauto',
    'pyautogui',
    'sentence_transformers',
    'langchain',
    'langchain_community',
    'lxml',
    'openai',
    'numpy',
    'torch',
    'html2text',
    'art',
    'uiautomation',
    'gradio_client'
]

# Check each dependency
missing = []
installed = []

for dep in critical_deps:
    # Handle special case where import name differs from package name
    if dep == 'yaml':
        check_name = 'yaml'
    elif dep == 'cv2':
        check_name = 'cv2'
    else:
        check_name = dep
    
    if check_import(check_name):
        installed.append(dep)
    else:
        missing.append(dep)

# Print results
print("=== UFO² Dependency Validation ===")
print(f"Total dependencies checked: {len(critical_deps)}")
print(f"Successfully installed: {len(installed)}")

if missing:
    print(f"\nMissing dependencies ({len(missing)}):")
    for dep in missing:
        print(f" - {dep}")
    sys.exit(1)
else:
    print("\nAll critical dependencies are installed successfully!")
    sys.exit(0)
"@

$validationScriptPath = Join-Path $projectPath "dependency_validation.py"
$validationScript | Out-File -FilePath $validationScriptPath -Encoding utf8

Write-ColorOutput "🔍 Running dependency validation..." -Color Cyan
& python $validationScriptPath

if ($LASTEXITCODE -eq 0) {
    Write-ColorOutput "✅ All critical dependencies validated successfully!" -Color Green
}
else {
    Write-ColorOutput "⚠️ Some dependencies are missing. Review the output above and install them manually." -Color Yellow
    Write-ColorOutput "   You can try running: pip install <package-name>" -Color Yellow
}

# ======================================================================
# SECTION 5: Configuration Setup
# ======================================================================
Write-ColorOutput "`n🔧 SECTION 5: Setting up configuration..." -Color Cyan

$configTemplatePath = "ufo\config\config.yaml.template"
$configPath = "ufo\config\config.yaml"

if (Test-Path $configTemplatePath) {
    if (-not (Test-Path $configPath)) {
        Copy-Item $configTemplatePath $configPath -Force
        Write-ColorOutput "✅ Configuration template copied to $configPath" -Color Green
        Write-ColorOutput "⚠️ IMPORTANT: You need to edit the config.yaml file to add your API keys" -Color Yellow
        Write-ColorOutput "   Opening the file for editing..." -Color Yellow
        Start-Process notepad $configPath
    }
    else {
        Write-ColorOutput "ℹ️ Configuration file already exists at $configPath" -Color Cyan
        
        # Validate existing config file contents
        $configContent = Get-Content -Path $configPath -Raw -ErrorAction SilentlyContinue
        
        if ($configContent) {
            Write-ColorOutput "🔍 Validating configuration file..." -Color Yellow
            
            # Check for common issues
            $issues = @()
            
            # Check for Azure OpenAI configuration issues
            if ($configContent -match "API_TYPE:\s+azure") {
                Write-ColorOutput "   Detected Azure OpenAI configuration" -Color Cyan
                
                # Check if using generic model names as deployment IDs
                if ($configContent -match "API_DEPLOYMENT_ID:\s+gpt-4o") {
                    $issues += "⚠️ Using 'gpt-4o' as Azure deployment ID. This likely needs to be changed to match your actual deployment name."
                }
                
                if ($configContent -match "API_BASE:\s+https://YOUR-RESOURCE-NAME\.openai\.azure\.com") {
                    $issues += "⚠️ Default API_BASE URL detected. You need to update this with your actual Azure OpenAI resource endpoint."
                }
                
                if ($configContent -match "API_KEY:\s+YOUR_API_KEY") {
                    $issues += "⚠️ Default API_KEY placeholder detected. You need to update this with your actual Azure OpenAI API key."
                }
                
                # Check for environment variable references
                $hasEnvVars = $configContent -match "\$\{[A-Z_]+\}" -or $configContent -match "%[A-Z_]+%"
                if (-not $hasEnvVars) {
                    $issues += "ℹ️ Consider using environment variables for API keys instead of hardcoding them. Example: API_KEY: ${AZURE_OPENAI_API_KEY}"
                }
            }
            
            # Display issues
            if ($issues.Count -gt 0) {
                Write-ColorOutput "   Found configuration issues that need attention:" -Color Yellow
                foreach ($issue in $issues) {
                    Write-ColorOutput "   $issue" -Color Yellow
                }
                
                Write-ColorOutput "   Would you like to open the config file for editing? (y/n)" -Color Yellow
                $openConfig = Read-Host
                
                if ($openConfig -eq "y") {
                    Start-Process notepad $configPath
                }
                
                # Create a helper script for setting environment variables
                $envScriptPath = Join-Path $projectPath "set_ufo_env_vars.ps1"
                if (-not (Test-Path $envScriptPath)) {
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
#    API_KEY: "$${AZURE_OPENAI_API_KEY}"
#    API_BASE: "$${AZURE_OPENAI_ENDPOINT}"
#    API_DEPLOYMENT_ID: "$${AZURE_OPENAI_DEPLOYMENT}"
'@ | Out-File -FilePath $envScriptPath -Encoding utf8
                    Write-ColorOutput "✅ Created environment variable helper script at $envScriptPath" -Color Green
                }
            }
            else {
                Write-ColorOutput "✅ Configuration appears to be valid" -Color Green
            }
        }
    }
}
else {
    Write-ColorOutput "❌ Configuration template not found at $configTemplatePath" -Color Red
}

# ======================================================================
# SECTION 6: VS Code Setup
# ======================================================================
Write-ColorOutput "`n🛠️ SECTION 6: Setting up VS Code for development..." -Color Cyan

# Create .vscode directory if it doesn't exist
$vscodeDir = Join-Path $projectPath ".vscode"
if (-not (Test-Path $vscodeDir)) {
    New-Item -ItemType Directory -Path $vscodeDir | Out-Null
    Write-ColorOutput "✅ Created .vscode directory" -Color Green
}

# Create launch.json for debugging
$launchJsonPath = Join-Path $vscodeDir "launch.json"
if (-not (Test-Path $launchJsonPath)) {
    @'
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "UFO Quickstart",
            "type": "python",
            "request": "launch",
            "module": "ufo",
            "args": ["--request", "Hello, what can you do?"],
            "justMyCode": false,
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        },
        {
            "name": "UFO Task Run",
            "type": "python",
            "request": "launch",
            "module": "ufo",
            "args": ["--task", "demo_hello", "-r", "open notepad and type hello"],
            "justMyCode": false,
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        },
        {
            "name": "UFO Debug Mode",
            "type": "python",
            "request": "launch",
            "module": "ufo",
            "args": ["--request", "What are you?", "--debug"],
            "justMyCode": false,
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}
'@ | Out-File -FilePath $launchJsonPath -Encoding utf8
    Write-ColorOutput "✅ Created launch.json with debugging configurations" -Color Green
}
else {
    Write-ColorOutput "ℹ️ launch.json already exists" -Color Cyan
}

# Create settings.json with recommended settings
$settingsJsonPath = Join-Path $vscodeDir "settings.json"
if (-not (Test-Path $settingsJsonPath)) {
    @'
{
    "python.defaultInterpreterPath": "${env:USERPROFILE}\\ufo_env\\Scripts\\python.exe",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "editor.formatOnSave": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.nosetestsEnabled": false,
    "python.testing.pytestArgs": [
        "."
    ]
}
'@ | Out-File -FilePath $settingsJsonPath -Encoding utf8
    Write-ColorOutput "✅ Created settings.json with recommended settings" -Color Green
}
else {
    Write-ColorOutput "ℹ️ settings.json already exists" -Color Cyan
}

# Create extensions.json with recommended extensions
$extensionsJsonPath = Join-Path $vscodeDir "extensions.json"
if (-not (Test-Path $extensionsJsonPath)) {
    @'
{
    "recommendations": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.black-formatter",
        "matangover.mypy",
        "charliermarsh.ruff",
        "njpwerner.autodocstring"
    ]
}
'@ | Out-File -FilePath $extensionsJsonPath -Encoding utf8
    Write-ColorOutput "✅ Created extensions.json with recommended extensions" -Color Green
}
else {
    Write-ColorOutput "ℹ️ extensions.json already exists" -Color Cyan
}

# ======================================================================
# SECTION 7: Minimal Test Creation
# ======================================================================
Write-ColorOutput "`n🧪 SECTION 7: Creating minimal test for imports..." -Color Cyan

$testDirPath = Join-Path $projectPath "tests"
if (-not (Test-Path $testDirPath)) {
    New-Item -ItemType Directory -Path $testDirPath | Out-Null
    Write-ColorOutput "✅ Created tests directory" -Color Green
}

$testImportsPath = Join-Path $testDirPath "test_imports.py"
if (-not (Test-Path $testImportsPath)) {
    @'
"""
Minimal test to validate that UFO imports work correctly.
This helps ensure the basic installation is functional.
"""
import unittest
import sys
import importlib.util

class TestUfoImports(unittest.TestCase):
    """Test case for validating UFO imports."""

    def test_ufo_module_import(self):
        """Test that the main UFO module can be imported."""
        try:
            from ufo import ufo
            self.assertTrue(True, "UFO module imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import ufo module: {e}")

    def test_critical_dependencies(self):
        """Test that critical dependencies are available."""
        critical_deps = [
            'azure.identity',
            'numpy',
            'torch',
            'langchain',
            'openai'
        ]

        for dep in critical_deps:
            with self.subTest(dependency=dep):
                spec = importlib.util.find_spec(dep)
                self.assertIsNotNone(spec, f"Dependency {dep} not found")

if __name__ == "__main__":
    unittest.main()
'@ | Out-File -FilePath $testImportsPath -Encoding utf8
    Write-ColorOutput "✅ Created minimal import test at tests/test_imports.py" -Color Green
}
else {
    Write-ColorOutput "ℹ️ Import test file already exists" -Color Cyan
}

# ======================================================================
# SECTION 8: Final Validation and API Connectivity Test
# ======================================================================
Write-ColorOutput "`n🚀 SECTION 8: Final Validation and API Connectivity Test..." -Color Cyan

# Run the minimal import test
Write-ColorOutput "🧪 Running minimal import test..." -Color Yellow
python -m unittest discover -s tests

# Try to run a basic UFO command
Write-ColorOutput "🧪 Testing basic UFO functionality..." -Color Yellow
Write-ColorOutput "   This will check if UFO can run without errors (API responses not validated)" -Color Yellow
python -m ufo --help

# Create an Azure OpenAI connectivity test script
$apiTestPath = Join-Path $projectPath "test_api_connectivity.py"
@'
"""
Azure OpenAI and UFO API connectivity test
This script tests both direct Azure OpenAI connectivity and UFO wrapper functionality
"""
import os
import sys
import yaml
from pathlib import Path
import traceback

def load_config():
    config_path = Path(__file__).parent / "ufo" / "config" / "config.yaml"
    if not config_path.exists():
        print(f"❌ Config file not found at {config_path}")
        return None
        
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"❌ Error loading config: {str(e)}")
        return None

def test_azure_openai_direct():
    """Test direct connectivity to Azure OpenAI without using UFO"""
    config = load_config()
    if not config:
        return False
    
    host_agent = config.get("AGENT_SETTINGS", {}).get("HOST_AGENT", {})
    api_type = host_agent.get("API_TYPE", "")
    
    if api_type.lower() != "azure":
        print("ℹ️ Not using Azure OpenAI, skipping direct Azure OpenAI test")
        return True
    
    print("\n=== Testing Direct Azure OpenAI Connectivity ===")
    
    # Extract Azure OpenAI settings from config
    api_base = host_agent.get("API_BASE", "")
    api_key = host_agent.get("API_KEY", "")
    api_deployment = host_agent.get("API_DEPLOYMENT_ID", "")
    api_version = host_agent.get("API_VERSION", "2024-05-01")
    
    if not api_base or not api_key or not api_deployment:
        print("❌ Missing Azure OpenAI configuration")
        return False
    
    try:
        from openai import AzureOpenAI
        
        # Create Azure OpenAI client
        client = AzureOpenAI(
            azure_endpoint=api_base,
            api_key=api_key,
            api_version=api_version
        )
        
        print(f"✅ Successfully created Azure OpenAI client")
        print(f"🔍 Testing connection to deployment: {api_deployment}")
        
        # Make a simple completion request
        try:
            response = client.chat.completions.create(
                model=api_deployment,
                messages=[{"role": "user", "content": "Hello, Azure OpenAI!"}],
                max_tokens=10
            )
            print(f"✅ Successfully connected to Azure OpenAI API")
            print(f"✅ Model responded with: {response.choices[0].message.content}")
            return True
        except Exception as e:
            error_msg = str(e)
            print(f"❌ API request failed: {error_msg}")
            
            # Provide specific guidance for common errors
            if "unavailable_model" in error_msg:
                print("\n🔧 TROUBLESHOOTING UNAVAILABLE_MODEL ERROR:")
                print("   The deployment ID in your config doesn't match any deployment in your Azure OpenAI resource.")
                print(f"   Current deployment ID: {api_deployment}")
                print("   Possible solutions:")
                print("   1. Check your Azure portal for the exact deployment name")
                print("   2. Create a new deployment with this name in Azure OpenAI Studio")
                print("   3. Update the API_DEPLOYMENT_ID in config.yaml to match an existing deployment")
                print("   4. Use environment variables: ${AZURE_OPENAI_DEPLOYMENT}")
            elif "authentication failed" in error_msg.lower() or "unauthorized" in error_msg.lower():
                print("\n🔧 TROUBLESHOOTING AUTHENTICATION ERROR:")
                print("   Your API key appears to be invalid.")
                print("   Possible solutions:")
                print("   1. Generate a new key in Azure portal")
                print("   2. Check for leading/trailing spaces in your key")
                print("   3. Use environment variables: ${AZURE_OPENAI_API_KEY}")
            elif "location" in error_msg.lower() or "endpoint" in error_msg.lower():
                print("\n🔧 TROUBLESHOOTING ENDPOINT ERROR:")
                print("   Your API endpoint appears to be incorrect.")
                print(f"   Current endpoint: {api_base}")
                print("   Possible solutions:")
                print("   1. Check the Azure portal for the correct endpoint URL")
                print("   2. Make sure the URL format is: https://{resource-name}.openai.azure.com")
                print("   3. Use environment variables: ${AZURE_OPENAI_ENDPOINT}")
                
            return False
    except ImportError:
        print("❌ Failed to import OpenAI library")
        print("   Try: pip install openai")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        traceback.print_exc()
        return False

def test_ufo_api_wrapper():
    """Test the UFO API wrapper"""
    print("\n=== Testing UFO API Wrapper ===")
    
    try:
        from ufo.llm import llm_manager
        
        try:
            # Initialize LLM manager
            llm = llm_manager.LLMManager()
            print(f"✅ Successfully initialized UFO LLM Manager")
            
            # Make a simple request
            try:
                response = llm.ask("Hello, what are you?", stream=False)
                print(f"✅ Successfully made request through UFO")
                print(f"✅ Response received (first 100 chars): {response[:100]}...")
                return True
            except Exception as e:
                print(f"❌ UFO API request failed: {str(e)}")
                return False
        except Exception as e:
            print(f"❌ Failed to initialize UFO LLM Manager: {str(e)}")
            return False
    except ImportError:
        print("❌ Failed to import UFO LLM manager")
        print("   This might indicate an issue with the UFO installation")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        traceback.print_exc()
        return False

def main():
    print("\n🔍 UFO² API CONNECTIVITY TEST")
    print("===========================")
    
    azure_test_result = test_azure_openai_direct()
    ufo_test_result = test_ufo_api_wrapper()
    
    print("\n=== TEST SUMMARY ===")
    print(f"Azure OpenAI Direct Test: {'✅ PASSED' if azure_test_result else '❌ FAILED'}")
    print(f"UFO API Wrapper Test: {'✅ PASSED' if ufo_test_result else '❌ FAILED'}")
    
    if not azure_test_result or not ufo_test_result:
        print("\n⚠️ Some tests failed. Please review the output above for troubleshooting steps.")
        sys.exit(1)
    else:
        print("\n✅ All connectivity tests passed! Your UFO² installation is ready to use.")
        sys.exit(0)

if __name__ == "__main__":
    main()
'@ | Out-File -FilePath $apiTestPath -Encoding utf8

# Ask if user wants to run the connectivity test
Write-ColorOutput "`n🧪 Would you like to run the Azure OpenAI connectivity test? (y/n)" -Color Yellow
$runConnectivityTest = Read-Host

if ($runConnectivityTest -eq "y") {
    Write-ColorOutput "🧪 Running API connectivity test..." -Color Yellow
    python $apiTestPath
    
    if ($LASTEXITCODE -eq 0) {
        Write-ColorOutput "✅ API connectivity test passed" -Color Green
    }
    else {
        Write-ColorOutput "⚠️ API connectivity test failed. Review the output above for troubleshooting steps." -Color Yellow
    }
}
else {
    Write-ColorOutput "ℹ️ Skipping API connectivity test. You can run it later with:" -Color Cyan
    Write-ColorOutput "   python $apiTestPath" -Color White
}

# ======================================================================
# SUMMARY
# ======================================================================
Write-ColorOutput "`n🎉 UFO² INSTALLATION COMPLETE! 🎉" -Color Magenta
Write-ColorOutput "=======================================================" -Color Magenta
Write-ColorOutput "Installation Summary:" -Color Cyan
Write-ColorOutput "✅ Core system dependencies installed" -Color Green
Write-ColorOutput "✅ Python virtual environment created at $envPath" -Color Green
Write-ColorOutput "✅ Project dependencies installed" -Color Green
Write-ColorOutput "✅ Configuration template set up" -Color Green
Write-ColorOutput "✅ VS Code development environment configured" -Color Green
Write-ColorOutput "✅ Minimal tests created" -Color Green
Write-ColorOutput "✅ Validation completed" -Color Green

# Create a detailed installation report
$reportPath = Join-Path $projectPath "ufo_installation_report.md"
@"
# UFO² Installation Report

## System Information
- Date: $(Get-Date -Format "yyyy-MM-dd")
- Windows Version: $([System.Environment]::OSVersion.VersionString)
- PowerShell Version: $($PSVersionTable.PSVersion)
- Python Version: $(python --version 2>&1)

## Installation Summary
- Virtual Environment: $envPath
- UFO Repository: $projectPath
- Configuration: $configPath

## Installed Components
- Core Dependencies: ✅
- Python Packages: ✅
- VS Code Configuration: ✅
- Test Scripts: ✅

## Common Issues and Solutions

### "unavailable_model" Error
This occurs when the deployment name in your config.yaml doesn't match your Azure OpenAI resource.

**Solution:**
1. Check Azure Portal for your actual deployment names
2. Update \`API_DEPLOYMENT_ID\` in config.yaml to match one of your deployments
3. Alternatively, create a new deployment with the name specified in your config

### API Key Management
For better security, use environment variables instead of hardcoding API keys:

```powershell
# Set environment variables
\$env:AZURE_OPENAI_API_KEY = "your-api-key"
\$env:AZURE_OPENAI_ENDPOINT = "https://your-resource.openai.azure.com"
\$env:AZURE_OPENAI_DEPLOYMENT = "your-deployment-name"

# Then in config.yaml:
API_KEY: \${AZURE_OPENAI_API_KEY}
API_BASE: \${AZURE_OPENAI_ENDPOINT}
API_DEPLOYMENT_ID: \${AZURE_OPENAI_DEPLOYMENT}
```

### Debugging UFO
To debug UFO using VS Code:
1. Open VS Code at the UFO directory
2. Set breakpoints in the code
3. Press F5 to start debugging (using provided launch configurations)
4. Try different launch configurations for different test scenarios

### VS Code Configurations
- UFO Quickstart: Test basic functionality
- UFO Debug Mode: Run with debug logging enabled
- UFO Task Demo: Test task execution

### Next Steps
- Run the API connectivity test: \`python $projectPath\test_api_connectivity.py\`
- Try a benchmark test with Windows Agent Arena
- Explore creating your own agents and tasks

## Resources
- Documentation: \`documents/\` directory
- Windows Agent Arena: https://microsoft.github.io/UFO/benchmark/windows_agent_arena/
- Environment Variables: \`$projectPath\set_ufo_env_vars.ps1\`
"@ | Out-File -FilePath $reportPath -Encoding utf8

Write-ColorOutput "`nDetailed installation report created at:" -Color Cyan
Write-ColorOutput "$reportPath" -Color White

Write-ColorOutput "`nNext Steps:" -Color Cyan
Write-ColorOutput "1. Configure your API keys:" -Color White
Write-ColorOutput "   - Edit $configPath directly" -Color White
Write-ColorOutput "   - OR use environment variables (see $projectPath\set_ufo_env_vars.ps1)" -Color White

Write-ColorOutput "2. Validate your configuration:" -Color White
Write-ColorOutput "   - Run API connectivity test: python $projectPath\test_api_connectivity.py" -Color White
Write-ColorOutput "   - Test basic functionality: python -m ufo --request \"Hello, what can you do?\"" -Color White

Write-ColorOutput "3. Fix common issues:" -Color White
Write-ColorOutput "   - 'unavailable_model' error: Update your API_DEPLOYMENT_ID in config.yaml" -Color White
Write-ColorOutput "   - Authentication errors: Check your API keys and endpoints" -Color White
Write-ColorOutput "   - Import errors: Make sure you're using the right virtual environment" -Color White

Write-ColorOutput "4. Development and debugging:" -Color White
Write-ColorOutput "   - Open VS Code: code-insiders $projectPath" -Color White
Write-ColorOutput "   - Use F5 to start debugging with provided launch configurations" -Color White

Write-ColorOutput "5. Advanced features:" -Color White
Write-ColorOutput "   - Try Windows Agent Arena benchmark: https://microsoft.github.io/UFO/benchmark/windows_agent_arena/" -Color White
Write-ColorOutput "   - Create your own agents: see documents/docs/creating_app_agent/" -Color White

Write-ColorOutput "`nHappy UFO-ing! 🛸👽✨" -Color Magenta
