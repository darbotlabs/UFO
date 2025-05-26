#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
UFO² Quick Validation Check
Created: 2025-05-25

This script performs a quick validation of the UFO² installation,
checking key dependencies and configuration.
"""

import os
import sys
import importlib.util
from pathlib import Path
import traceback


# ANSI color codes for output formatting
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
END = "\033[0m"
BOLD = "\033[1m"


def print_header(text):
    """Print a formatted section header."""
    print(f"\n{BOLD}{BLUE}{'=' * 60}{END}")
    print(f"{BOLD}{BLUE}  {text}{END}")
    print(f"{BOLD}{BLUE}{'=' * 60}{END}")


def print_success(text):
    """Print a success message."""
    print(f"{GREEN}✅ {text}{END}")


def print_warning(text):
    """Print a warning message."""
    print(f"{YELLOW}⚠️ {text}{END}")


def print_error(text):
    """Print an error message."""
    print(f"{RED}❌ {text}{END}")


def print_info(text):
    """Print an info message."""
    print(f"{CYAN}ℹ️ {text}{END}")


def check_dependency(module_name):
    """Check if a Python module is installed and importable."""
    try:
        if "." in module_name:
            base_module = module_name.split(".")[0]
            importlib.import_module(base_module)
            try:
                importlib.import_module(module_name)
                return True, f"{module_name} successfully imported"
            except ImportError as e:
                return False, f"Failed to import submodule {module_name}: {str(e)}"
        else:
            importlib.import_module(module_name)
            return True, f"{module_name} successfully imported"
    except ImportError as e:
        return False, f"Import error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"


def check_critical_dependencies():
    """Check critical dependencies required by UFO."""
    print_header("Critical Dependency Check")

    # Critical dependencies
    critical_deps = [
        "azure.identity",
        "openai",
        "faiss",
        "cv2",
        "yaml",
        "numpy",
        "pywinauto",
        "pyautogui",
        "torch",
    ]

    all_ok = True
    missing_deps = []

    for dep in critical_deps:
        success, message = check_dependency(dep)
        if success:
            print_success(message)
        else:
            all_ok = False
            missing_deps.append(dep)
            print_error(message)

    if all_ok:
        print_success("\nAll critical dependencies are installed.")
    else:
        print_error(f"\nMissing dependencies: {', '.join(missing_deps)}")
        print_info("Run: pip install " + " ".join(missing_deps))

    return all_ok


def check_ufo_imports():
    """Check if UFO modules can be imported."""
    print_header("UFO Import Test")
    
    try:
        import ufo
        print_success("Successfully imported UFO main package")
        
        try:
            from ufo import ufo as ufo_module
            print_success("Successfully imported UFO module")
        except ImportError as e:
            print_error(f"Failed to import UFO module: {e}")
            return False
            
        return True
    except ImportError as e:
        print_error(f"Failed to import UFO package: {e}")
        return False


def check_config():
    """Check if config file exists and has basic structure."""
    print_header("Config Check")
    
    project_root = Path(__file__).parent
    config_path = project_root / "ufo" / "config" / "config.yaml"
    
    if not config_path.exists():
        print_error(f"Config file not found: {config_path}")
        return False
    
    try:
        import yaml
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            
        if not config:
            print_error("Config file is empty or invalid YAML")
            return False
            
        if "HOST_AGENT" not in config:
            print_error("Missing HOST_AGENT section in config")
            return False
            
        host_agent = config["HOST_AGENT"]
        
        required_fields = ["API_TYPE", "API_KEY", "API_BASE"]
        missing_fields = []
        
        for field in required_fields:
            if field not in host_agent:
                missing_fields.append(field)
                
        if missing_fields:
            print_error(f"Missing required fields in HOST_AGENT config: {', '.join(missing_fields)}")
            return False
            
        # Check for Azure OpenAI specific settings
        api_type = host_agent["API_TYPE"].lower()
        if api_type in ["aoai", "azure"]:
            print_info("Found Azure OpenAI configuration")
            
            if "API_DEPLOYMENT_ID" not in host_agent:
                print_warning("Missing API_DEPLOYMENT_ID in Azure configuration")
                
            deployment_id = host_agent.get("API_DEPLOYMENT_ID", "")
            if deployment_id in ["gpt-4", "gpt-4o", "gpt-35-turbo", "gpt-3.5-turbo"]:
                print_warning(f"API_DEPLOYMENT_ID '{deployment_id}' looks like a model name, not a deployment name")
                print_info("In Azure OpenAI, you need to use your actual deployment name, not the model name")
                
        print_success("Config file has basic required structure")
        return True
        
    except ImportError:
        print_error("Failed to import yaml module")
        print_info("Run: pip install pyyaml")
        return False
    except Exception as e:
        print_error(f"Error checking config: {str(e)}")
        traceback.print_exc()
        return False


def check_azure_deployment():
    """Check Azure OpenAI deployment configuration if applicable."""
    print_header("Azure OpenAI Deployment Check")
    
    try:
        import yaml
        
        project_root = Path(__file__).parent
        config_path = project_root / "ufo" / "config" / "config.yaml"
        
        if not config_path.exists():
            print_error("Config file not found")
            return False
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            
        if "HOST_AGENT" not in config:
            print_error("Missing HOST_AGENT section in config")
            return False
            
        host_agent = config["HOST_AGENT"]
        api_type = host_agent.get("API_TYPE", "").lower()
        
        if api_type not in ["aoai", "azure"]:
            print_info("Not using Azure OpenAI, skipping deployment check")
            return True
        
        print_info("Would you like to test Azure OpenAI connectivity? (y/n)")
        choice = input().strip().lower()
        
        if choice != 'y':
            print_info("Skipping Azure OpenAI connectivity test")
            return True
        
        # Try a basic connection test
        try:
            from openai import AzureOpenAI
            
            api_base = host_agent["API_BASE"]
            api_key = host_agent["API_KEY"]
            api_version = host_agent.get("API_VERSION", "2024-02-15-preview")
            deployment_id = host_agent.get("API_DEPLOYMENT_ID", "")
            
            print_info(f"Testing connection to {api_base} with deployment {deployment_id}")
            
            client = AzureOpenAI(
                azure_endpoint=api_base,
                api_key=api_key,
                api_version=api_version
            )
            
            response = client.chat.completions.create(
                model=deployment_id,
                messages=[{"role": "user", "content": "Say hello"}],
                max_tokens=10
            )
            
            print_success("Successfully connected to Azure OpenAI API")
            print_info(f"Response: {response.choices[0].message.content}")
            return True
            
        except Exception as e:
            print_error(f"Azure OpenAI connection failed: {str(e)}")
            
            error_str = str(e).lower()
            if "unavailable_model" in error_str or "not found" in error_str:
                print_warning("The deployment name in your config doesn't match any deployment in your Azure OpenAI resource")
                print_info(f"Current deployment ID: {deployment_id}")
                print_info("Check Azure Portal for your actual deployment names")
                print_info("For example, if your deployment is named 'gpt4o', use that instead of 'gpt-4o'")
                
            return False
            
    except ImportError as e:
        print_error(f"Import error: {str(e)}")
        return False
    except Exception as e:
        print_error(f"Error during Azure deployment check: {str(e)}")
        traceback.print_exc()
        return False


def main():
    """Run validation checks."""
    print(f"{BOLD}{YELLOW}UFO² QUICK VALIDATION CHECK{END}")
    print(f"{YELLOW}{'=' * 60}{END}")
    print(f"{CYAN}Date: {END}{BOLD}{CYAN}2025-05-25{END}")
    print(f"{CYAN}Python: {END}{BOLD}{CYAN}{sys.version.split()[0]}{END}")
    print(f"{YELLOW}{'=' * 60}{END}\n")
    
    # Run checks
    dep_check = check_critical_dependencies()
    import_check = check_ufo_imports()
    config_check = check_config()
    azure_check = check_azure_deployment()
    
    # Final summary
    print_header("Validation Summary")
    
    tests = [
        ("Critical Dependencies", dep_check),
        ("UFO Imports", import_check),
        ("Config Structure", config_check),
        ("Azure Deployment", azure_check)
    ]
    
    for name, result in tests:
        if result:
            print_success(f"{name}: PASS")
        else:
            print_error(f"{name}: FAIL")
    
    all_ok = all(result for _, result in tests)
    
    if all_ok:
        print(f"\n{BOLD}{GREEN}UFO² VALIDATION SUCCESSFUL! 🎉{END}")
        print_success("Your UFO² installation appears to be correctly set up.")
        return 0
    else:
        print(f"\n{BOLD}{YELLOW}UFO² VALIDATION PARTIALLY SUCCESSFUL{END}")
        print_warning("Some checks failed. Review the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
