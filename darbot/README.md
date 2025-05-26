# DARBOT - UFO² Installation and Validation Pack
**Created:** May 25, 2025  
**Version:** 1.0.0

## Overview
This pack contains a comprehensive set of scripts and documentation for installing, configuring, and validating the UFO² (Universal Framework for Operation) desktop agent framework. DARBOT provides a streamlined approach to setting up UFO² on Windows environments with proper validation and troubleshooting.

## Project Components

### Core Installation
- **`install_ufo_dependencies.ps1`**: Complete PowerShell script for installing all dependencies required for UFO²
- **`requirements.txt`**: Python package dependencies for the UFO² framework
- **`set_ufo_env_vars.ps1`**: Helper script for configuring environment variables (created by installation script)

### Validation Tools
- **`quick_check.py`**: Fast validation script to verify basic UFO² functionality
- **`comprehensive_validation.py`**: Thorough validation of all UFO² components
- **`test_api_connectivity.py`**: Tests Azure OpenAI or OpenAI API connectivity
- **`test_mission.py`**: Simple validation script for checking UFO² imports
- **`fix_azure_config.py`**: Helper script to fix Azure OpenAI deployment configuration issues

### Documentation
- **`updated_mission_pack.md`**: Enhanced mission documentation with comprehensive setup instructions
- **`mission_report_2025-05-01.md`**: Report on setup completion and encountered issues
- **`FullStepsandTroubleshooting.md`**: Detailed walkthrough with additional troubleshooting guidance

## Installation Guide

### Prerequisites
- Windows 10/11 machine
- Administrator access
- Internet connection
- PowerShell 7+ recommended

### Quick Start

1. **Open PowerShell 7 as Administrator**
   ```powershell
   # Check your PowerShell version first
   $PSVersionTable.PSVersion
   ```

2. **Run the Installation Script**
   ```powershell
   cd g:\Github\UFO
   .\install_ufo_dependencies.ps1
   ```

3. **Validate Installation**
   ```powershell
   # Quick validation
   python .\quick_check.py
   
   # Comprehensive validation
   python .\comprehensive_validation.py
   
   # Test API connectivity (if configured)
   python .\test_api_connectivity.py
   ```

### Configuration Steps

1. **Configure your `config.yaml`**  
   The installation script will create this file from the template if it doesn't exist.
   
   Important settings for Azure OpenAI:
   ```yaml
   API_TYPE: "azure"  # or "aoai" depending on template
   API_BASE: "https://your-resource-name.openai.azure.com/"
   API_KEY: "your-api-key"
   API_VERSION: "2024-02-15-preview"
   API_DEPLOYMENT_ID: "your-deployment-name"  # NOT "gpt-4o" - use your actual deployment name
   ```

2. **Set Environment Variables (Recommended)**
   ```powershell
   # Run the environment variables helper script
   .\set_ufo_env_vars.ps1
   
   # Edit the script first with your actual values
   notepad .\set_ufo_env_vars.ps1
   ```

3. **Fix Azure OpenAI Configuration Issues**
   ```powershell
   # If you encounter "unavailable_model" errors
   python .\fix_azure_config.py
   ```

## Troubleshooting Guide

### Common Issues

#### "unavailable_model: gpt-4o" Error
This occurs when your `API_DEPLOYMENT_ID` in the config.yaml is set to a model name ("gpt-4o") instead of your actual Azure OpenAI deployment name.

**Solution:**
1. Open your Azure OpenAI Studio
2. Note the actual deployment name of your GPT-4o model
3. Update config.yaml with this exact deployment name
4. Alternatively, run `python .\fix_azure_config.py` to fix this automatically

#### Import Errors
If Python modules fail to import:

**Solution:**
1. Verify virtual environment is activated
   ```powershell
   # Activate the virtual environment
   & "$env:USERPROFILE\ufo_env\Scripts\Activate.ps1"
   ```
2. Install missing packages
   ```powershell
   pip install -r requirements.txt
   ```

#### VS Code Debugging Issues
If debugging doesn't work in VS Code:

**Solution:**
1. Ensure VS Code is using the correct Python interpreter
2. Check launch.json configurations
3. Set PYTHONPATH in your environment or in launch.json

## Using UFO² Framework

### Basic Commands

Test a simple request:
```powershell
python -m ufo --request "Hello, what can you do?"
```

Run with debug logging:
```powershell
python -m ufo --request "Hello, what can you do?" --debug
```

Execute a task:
```powershell
python -m ufo --task demo_hello -r "open notepad and type hello"
```

### VS Code Integration

Launch VS Code with:
```powershell
code-insiders g:\Github\UFO
```

Use the provided launch configurations for debugging:
- UFO Quickstart
- UFO Task Run
- UFO Debug Mode

## Directory Organization

Consider organizing all DARBOT files into a dedicated folder:
```powershell
# Create a darbot folder
New-Item -Path "g:\Github\UFO\darbot" -ItemType Directory -Force

# Copy all DARBOT files
Copy-Item -Path "g:\Github\UFO\install_ufo_dependencies.ps1" -Destination "g:\Github\UFO\darbot\"
Copy-Item -Path "g:\Github\UFO\quick_check.py" -Destination "g:\Github\UFO\darbot\"
Copy-Item -Path "g:\Github\UFO\comprehensive_validation.py" -Destination "g:\Github\UFO\darbot\"
Copy-Item -Path "g:\Github\UFO\test_api_connectivity.py" -Destination "g:\Github\UFO\darbot\"
Copy-Item -Path "g:\Github\UFO\fix_azure_config.py" -Destination "g:\Github\UFO\darbot\"
Copy-Item -Path "g:\Github\UFO\test_mission.py" -Destination "g:\Github\UFO\darbot\"
Copy-Item -Path "g:\Github\UFO\updated_mission_pack.md" -Destination "g:\Github\UFO\darbot\"
Copy-Item -Path "g:\Github\UFO\mission_report_2025-05-01.md" -Destination "g:\Github\UFO\darbot\"
Copy-Item -Path "g:\Github\UFO\FullStepsandTroubleshooting.md" -Destination "g:\Github\UFO\darbot\"
Copy-Item -Path "g:\Github\UFO\DARBOT_README.md" -Destination "g:\Github\UFO\darbot\README.md"

# Run your scripts from the darbot folder
cd g:\Github\UFO\darbot
.\install_ufo_dependencies.ps1
```

## Documentation References
- [UFO² Official Documentation](https://microsoft.github.io/UFO)
- [Mission Pack](g:\Github\UFO\updated_mission_pack.md)
- [Full Steps and Troubleshooting](g:\Github\UFO\FullStepsandTroubleshooting.md)

## Project Structure
The installation validates and ensures the following project structure is correct:
```
ufo/
  ├── agents/        # Agent implementations
  ├── automator/     # OS automation tools
  ├── config/        # Configuration files
  ├── llm/           # LLM implementations
  ├── prompter/      # Prompt generation
  ├── prompts/       # Prompt templates
  ├── utils/         # Utility functions
  ├── __init__.py    # Package initialization
  ├── __main__.py    # Entry point
  └── ufo.py         # Core UFO class
```

## Credits
- DARBOT Installation Pack: Windows Agent Arena Team
- UFO² Framework: Microsoft Corporation