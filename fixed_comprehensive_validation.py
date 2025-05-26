#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
UFO² Comprehensive Validation Script
Created: 2025-05-25

This script performs a comprehensive validation of the UFO² installation,
checking dependencies, configuration, and functionality.
"""

import os
import sys
import importlib
import traceback
from pathlib import Path


class Colors:
    """Terminal colors for output formatting."""
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    END = "\033[0m"
    BOLD = "\033[1m"


def print_header(text):
    """Print a formatted section header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}  {text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.END}")


def print_success(text):
    """Print a success message."""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")


def print_warning(text):
    """Print a warning message."""
    print(f"{Colors.YELLOW}⚠️ {text}{Colors.END}")


def print_error(text):
    """Print an error message."""
    print(f"{Colors.RED}❌ {text}{Colors.END}")


def print_info(text):
    """Print an info message."""
    print(f"{Colors.CYAN}ℹ️ {text}{Colors.END}")


def check_critical_imports():
    """Check if critical Python packages are installed."""
    print_header("Critical Dependencies Check")
    
    critical_deps = [
        'azure.identity',
        'openai',
        'numpy',
        'yaml',
        'torch',
        'langchain',
        'langchain_community',
        'html2text',
        'art',
        'uiautomation',
        'gradio_client',
        'faiss',
        'pywinauto',
        'pyautogui'
    ]
    
    optional_deps = [
        'transformers',
        'sentence_transformers',
        'cv2',
        'lxml'
    ]
    
    success_count = 0
    failed_deps = []
    
    # Check critical dependencies
    for dep in critical_deps:
        try:
            if dep == 'yaml':
                # special case for pyyaml which imports as yaml
                import yaml
                print_success(f"{dep} successfully imported")
            elif dep == 'faiss':
                # special case for faiss-cpu which imports as faiss
                import faiss
                print_success(f"{dep} successfully imported")
            elif dep == 'cv2':
                # special case for opencv-python which imports as cv2
                import cv2
                print_success(f"{dep} successfully imported")
            else:
                # Try to import the module dynamically
                importlib.import_module(dep)
                print_success(f"{dep} successfully imported")
            success_count += 1
        except (ImportError, ModuleNotFoundError):
            print_error(f"{dep} not found")
            failed_deps.append(dep)
    
    # Check optional dependencies
    print("\n--- Optional Dependencies ---")
    optional_success = 0
    for dep in optional_deps:
        try:
            if dep == 'cv2':
                import cv2
                print_success(f"{dep} successfully imported")
            else:
                importlib.import_module(dep)
                print_success(f"{dep} successfully imported")
            optional_success += 1
        except (ImportError, ModuleNotFoundError):
            print_warning(f"{dep} not found (optional)")
    
    # Summary
    if failed_deps:
        print_error(f"\nMissing {len(failed_deps)} critical dependencies:")
        for dep in failed_deps:
            print_error(f"  - {dep}")
        print_info("Install missing dependencies with: pip install <package-name>")
        return False
    else:
        print_success(f"\nAll {success_count} critical dependencies are installed.")
        print_info(f"{optional_success}/{len(optional_deps)} optional dependencies are installed.")
        return True


def check_ufo_imports():
    """Check if the UFO package can be imported."""
    print_header("UFO Package Import Check")
    
    try:
        print_info("Attempting to import UFO package...")
        try:
            import ufo
            print_success("UFO package imported successfully")
            
            # Check UFO structure
            expected_modules = [
                'agents',
                'automator', 
                'config',
                'llm',
                'prompter',
                'prompts',
                'utils'
            ]
            
            missing_modules = []
            ufo_path = Path(ufo.__file__).parent
            
            for module in expected_modules:
                module_path = ufo_path / module
                if not module_path.exists():
                    missing_modules.append(module)
            
            if missing_modules:
                print_warning(f"Some expected UFO modules are missing: {', '.join(missing_modules)}")
            else:
                print_success("All expected UFO modules are present")
            
            return True
        except Exception as e:
            print_error(f"Error importing UFO: {str(e)}")
            print_info("Make sure the UFO package is properly installed")
            return False
    except Exception as e:
        print_error(f"Unexpected error during import check: {str(e)}")
        return False


def check_config_file():
    """Check if the config file exists and has the correct structure."""
    print_header("Configuration Check")
    
    # Check for config file
    config_path = Path(__file__).parent / "ufo" / "config" / "config.yaml"
    if not config_path.exists():
        print_error(f"Config file not found at {config_path}")
        print_info("You need to create a config.yaml file from the template")
        return False
    
    try:
        import yaml
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        if not config:
            print_error("Config file is empty or invalid")
            return False
        
        # Check for HOST_AGENT or AGENT_SETTINGS.HOST_AGENT
        host_agent = None
        if "HOST_AGENT" in config:
            host_agent = config["HOST_AGENT"]
            print_info("Found HOST_AGENT configuration")
        elif "AGENT_SETTINGS" in config and "HOST_AGENT" in config["AGENT_SETTINGS"]:
            host_agent = config["AGENT_SETTINGS"]["HOST_AGENT"]
            print_info("Found AGENT_SETTINGS.HOST_AGENT configuration")
        else:
            print_error("Could not find HOST_AGENT configuration")
            return False
        
        # Check required fields
        required_fields = ["API_TYPE", "API_BASE", "API_KEY"]
        missing_fields = []
        for field in required_fields:
            if field not in host_agent:
                missing_fields.append(field)
        
        if missing_fields:
            print_error(f"Missing required fields in configuration: {', '.join(missing_fields)}")
            return False
        
        # Check API type
        api_type = host_agent["API_TYPE"].lower()
        print_info(f"API Type: {api_type}")
        
        if api_type in ["azure", "aoai"]:
            print_info("Using Azure OpenAI")
            
            # Check Azure-specific settings
            if "API_DEPLOYMENT_ID" not in host_agent:
                print_error("API_DEPLOYMENT_ID is required for Azure OpenAI")
                return False
            
            # Check if deployment ID looks like a model name
            deployment_id = host_agent["API_DEPLOYMENT_ID"]
            if deployment_id.startswith("gpt-"):
                print_warning(f"API_DEPLOYMENT_ID '{deployment_id}' looks like a model name, not a deployment name")
                print_info("In Azure OpenAI, you need to use your actual deployment name, not the model name")
            
            # Check for environment variables
            api_key = host_agent["API_KEY"]
            if api_key.startswith("${") or api_key.startswith("%"):
                print_info("Using environment variables for API keys (recommended)")
            else:
                print_warning("Consider using environment variables for API keys instead of hardcoding them")
        
        print_success("Config file has required structure")
        return True
    
    except Exception as e:
        print_error(f"Error reading or parsing config file: {str(e)}")
        traceback.print_exc()
        return False


def check_virtual_env():
    """Check if running inside a virtual environment."""
    print_header("Virtual Environment Check")
    
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        venv_path = sys.prefix
        print_success(f"Running in virtual environment: {venv_path}")
        return True
    else:
        print_warning("Not running in a virtual environment")
        print_info("It's recommended to use UFO² within a virtual environment")
        return True  # Not critical


def check_api_connectivity():
    """Test connectivity to the configured API."""
    print_header("API Connectivity Test")
    
    config_path = Path(__file__).parent / "ufo" / "config" / "config.yaml"
    if not config_path.exists():
        print_error(f"Config file not found: {config_path}")
        return False
    
    try:
        print_info("This test will attempt to connect to the configured API")
        print_info("Would you like to continue? (y/n)")
        choice = input().strip().lower()
        if choice != 'y':
            print_warning("API test skipped by user")
            return True
            
        import yaml
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            
        # Find the host agent configuration
        host_agent = None
        if "HOST_AGENT" in config:
            host_agent = config["HOST_AGENT"]
        elif "AGENT_SETTINGS" in config and "HOST_AGENT" in config["AGENT_SETTINGS"]:
            host_agent = config["AGENT_SETTINGS"]["HOST_AGENT"]
        else:
            print_error("Could not find HOST_AGENT configuration")
            return False
            
        api_type = host_agent["API_TYPE"].lower()
        
        if api_type in ["azure", "aoai"]:
            # Test Azure OpenAI connectivity
            try:
                print_info("Testing Azure OpenAI connectivity...")
                from openai import AzureOpenAI
                
                # Get Azure OpenAI settings
                api_base = host_agent["API_BASE"]
                api_key = host_agent["API_KEY"]
                api_deployment = host_agent["API_DEPLOYMENT_ID"]
                api_version = host_agent.get("API_VERSION", "2024-02-15-preview")
                
                # Resolve environment variables
                if api_key.startswith("${") and api_key.endswith("}"):
                    env_var = api_key[2:-1]
                    api_key = os.environ.get(env_var, "")
                    if not api_key:
                        print_error(f"Environment variable {env_var} is not set")
                        return False
                
                if api_base.startswith("${") and api_base.endswith("}"):
                    env_var = api_base[2:-1]
                    api_base = os.environ.get(env_var, "")
                    if not api_base:
                        print_error(f"Environment variable {env_var} is not set")
                        return False
                
                if api_deployment.startswith("${") and api_deployment.endswith("}"):
                    env_var = api_deployment[2:-1]
                    api_deployment = os.environ.get(env_var, "")
                    if not api_deployment:
                        print_error(f"Environment variable {env_var} is not set")
                        return False
                
                # Create client
                client = AzureOpenAI(
                    azure_endpoint=api_base,
                    api_key=api_key,
                    api_version=api_version
                )
                
                print_info(f"Testing connection to deployment: {api_deployment}")
                
                response = client.chat.completions.create(
                    model=api_deployment,
                    messages=[{"role": "user", "content": "Say hello"}],
                    max_tokens=10
                )
                
                print_success("Successfully connected to Azure OpenAI API!")
                print_info(f"Response: {response.choices[0].message.content}")
                return True
                
            except Exception as e:
                error_msg = str(e)
                print_error(f"API test failed: {error_msg}")
                
                if "unavailable_model" in error_msg:
                    print_warning("\nThis appears to be an issue with your deployment ID.")
                    print_info("In Azure OpenAI, the deployment ID should be the name you gave your deployment in Azure portal")
                    print_info("For example, if you deployed GPT-4o with the name 'my-gpt4o', your deployment ID should be 'my-gpt4o'")
                
                return False
        
        elif api_type == "openai":
            # Test OpenAI connectivity
            try:
                print_info("Testing OpenAI connectivity...")
                from openai import OpenAI
                
                # Get OpenAI settings
                api_key = host_agent["API_KEY"]
                
                # Resolve environment variable if used
                if api_key.startswith("${") and api_key.endswith("}"):
                    env_var = api_key[2:-1]
                    api_key = os.environ.get(env_var, "")
                    if not api_key:
                        print_error(f"Environment variable {env_var} is not set")
                        return False
                
                # Create client
                client = OpenAI(api_key=api_key)
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": "Say hello"}],
                    max_tokens=10
                )
                
                print_success("Successfully connected to OpenAI API!")
                print_info(f"Response: {response.choices[0].message.content}")
                return True
                
            except Exception as e:
                print_error(f"API test failed: {str(e)}")
                return False
        
        else:
            print_error(f"Unsupported API type: {api_type}")
            return False
            
    except ModuleNotFoundError as e:
        print_error(f"Missing required package: {e}")
        print_info("Make sure all required packages are installed")
        return False
        
    except Exception as e:
        print_error(f"Error during API connectivity test: {str(e)}")
        traceback.print_exc()
        return False


def run_validation():
    """Run all validation checks."""
    print_header("UFO² COMPREHENSIVE VALIDATION")
    print(f"Date: 2025-05-25")
    print(f"Python: {sys.version.split()[0]}")
    
    # Results tracking
    results = {
        "dependencies": False,
        "imports": False,
        "config": False,
        "virtual_env": False,
        "api": False
    }
    
    # Run checks
    results["dependencies"] = check_critical_imports()
    results["imports"] = check_ufo_imports()
    results["config"] = check_config_file()
    results["virtual_env"] = check_virtual_env()
    results["api"] = check_api_connectivity()
    
    # Summary
    print_header("VALIDATION SUMMARY")
    
    for check, result in results.items():
        status = f"{Colors.GREEN}PASS{Colors.END}" if result else f"{Colors.RED}FAIL{Colors.END}"
        print(f"{check.capitalize()}: {status}")
    
    all_passed = all(results.values())
    if all_passed:
        print_success("\nAll validation checks passed!")
        print(f"\n{Colors.BOLD}{Colors.GREEN}UFO² VALIDATION SUCCESSFUL! 🎉{Colors.END}")
        print(f"{Colors.GREEN}Your UFO² installation is ready to use.{Colors.END}")
        return 0
    else:
        print_warning("\nSome validation checks failed. Review the output above for details.")
        print(f"\n{Colors.BOLD}{Colors.YELLOW}UFO² VALIDATION PARTIALLY SUCCESSFUL{Colors.END}")
        print(f"{Colors.YELLOW}Please fix the issues identified above before using UFO².{Colors.END}")
        return 1


if __name__ == "__main__":
    sys.exit(run_validation())
