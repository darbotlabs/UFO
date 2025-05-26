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


def check_all_dependencies():
    """Check all dependencies required by UFO."""
    print_header("Dependency Check")

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
        "sentence_transformers",
        "langchain",
        "lxml"
    ]

    # Optional but recommended dependencies
    optional_deps = [
        "pytest",
        "black",
        "ruff",
        "mypy",
        "ipykernel",
        "matplotlib",
    ]

    all_ok = True
    missing_critical = []
    missing_optional = []

    # Check critical dependencies
    print(f"\n{Colors.BOLD}Critical Dependencies:{Colors.END}")
    for dep in critical_deps:
        success, message = check_dependency(dep)
        if success:
            print_success(message)
        else:
            all_ok = False
            missing_critical.append(dep)
            print_error(message)

    # Check optional dependencies
    print(f"\n{Colors.BOLD}Optional Dependencies:{Colors.END}")
    for dep in optional_deps:
        success, message = check_dependency(dep)
        if success:
            print_success(message)
        else:
            missing_optional.append(dep)
            print_warning(message)

    # Summary
    print(f"\n{Colors.BOLD}Dependency Summary:{Colors.END}")
    if not missing_critical:
        print_success("All critical dependencies are installed.")
    else:
        print_error(f"Missing critical dependencies: {', '.join(missing_critical)}")
        print_info("Run: pip install " + " ".join(missing_critical))

    if missing_optional:
        print_warning(f"Missing optional dependencies: {', '.join(missing_optional)}")
        print_info("Run: pip install " + " ".join(missing_optional) + " (recommended)")

    return all_ok


def check_ufo_structure():
    """Check the UFO directory structure."""
    print_header("UFO Directory Structure Check")

    project_root = Path(__file__).parent
    ufo_dir = project_root / "ufo"

    if not ufo_dir.is_dir():
        print_error(f"UFO directory not found at {ufo_dir}")
        return False

    # Essential directories
    essential_dirs = [
        "agents",
        "automator",
        "config",
        "llm",
        "prompter",
        "prompts",
        "utils"
    ]

    # Essential files
    essential_files = [
        "__init__.py",
        "__main__.py",
        "ufo.py"
    ]

    # Check directories
    print(f"\n{Colors.BOLD}Essential Directories:{Colors.END}")
    all_dirs_ok = True
    for dir_name in essential_dirs:
        dir_path = ufo_dir / dir_name
        if dir_path.is_dir():
            print_success(f"Directory exists: ufo/{dir_name}")
        else:
            print_error(f"Missing directory: ufo/{dir_name}")
            all_dirs_ok = False

    # Check files
    print(f"\n{Colors.BOLD}Essential Files:{Colors.END}")
    all_files_ok = True
    for file_name in essential_files:
        file_path = ufo_dir / file_name
        if file_path.is_file():
            print_success(f"File exists: ufo/{file_name}")
        else:
            print_error(f"Missing file: ufo/{file_name}")
            all_files_ok = False

    # Check config file
    config_path = ufo_dir / "config" / "config.yaml"
    config_template_path = ufo_dir / "config" / "config.yaml.template"

    print(f"\n{Colors.BOLD}Configuration Files:{Colors.END}")
    if config_template_path.is_file():
        print_success(f"Config template exists: ufo/config/config.yaml.template")
    else:
        print_error(f"Missing config template: ufo/config/config.yaml.template")
        all_files_ok = False

    if config_path.is_file():
        print_success(f"Config file exists: ufo/config/config.yaml")
    else:
        print_warning(f"Config file not found: ufo/config/config.yaml")
        print_info(f"You need to create this file from the template.")
        all_files_ok = False

    # Summary
    print(f"\n{Colors.BOLD}Structure Check Summary:{Colors.END}")
    if all_dirs_ok and all_files_ok:
        print_success("UFO directory structure is valid.")
        return True
    else:
        print_error("UFO directory structure has issues.")
        return False


def validate_config():
    """Validate the UFO configuration."""
    print_header("Configuration Validation")

    config_path = Path(__file__).parent / "ufo" / "config" / "config.yaml"
    if not config_path.exists():
        print_error(f"Config file not found: {config_path}")
        print_info("Create config.yaml from config.yaml.template")
        return False

    try:
        import yaml
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        if not config:
            print_error("Config file is empty or invalid YAML")
            return False        # Check for HOST_AGENT
        if "HOST_AGENT" not in config:
            print_error("Missing HOST_AGENT in config")
            return False

        host_agent = config["HOST_AGENT"]

        # Check required API settings
        print(f"\n{Colors.BOLD}API Configuration:{Colors.END}")
        required_fields = ["API_TYPE", "API_KEY"]
        for field in required_fields:
            if field not in host_agent:
                print_error(f"Missing {field} in HOST_AGENT configuration")
                return False
            else:
                print_success(f"{field} is configured")

        # Azure OpenAI specific checks
        api_type = host_agent["API_TYPE"]
        if api_type.lower() == "azure":
            print(f"\n{Colors.BOLD}Azure OpenAI Configuration:{Colors.END}")

            azure_fields = ["API_BASE", "API_VERSION", "API_DEPLOYMENT_ID"]
            for field in azure_fields:
                if field not in host_agent:
                    print_error(f"Missing {field} in Azure configuration")
                    return False
                else:
                    print_success(f"{field} is configured")

            # Check for common Azure OpenAI configuration issues
            api_deployment = host_agent["API_DEPLOYMENT_ID"]
            api_base = host_agent["API_BASE"]

            if api_deployment in ["gpt-4", "gpt-4o", "gpt-35-turbo", "gpt-3.5-turbo"]:
                print_warning(f"API_DEPLOYMENT_ID '{api_deployment}' looks like a model name, not a deployment name")
                print_info("In Azure OpenAI, you need to use your actual deployment name, not the model name")
                print_info("Check Azure Portal or Azure OpenAI Studio for your deployment names")

            if "your-resource" in api_base.lower() or "your" in api_base.lower():
                print_error(f"API_BASE contains placeholder text: {api_base}")
                print_info("Replace with your actual Azure OpenAI endpoint URL")

            api_key = host_agent["API_KEY"]
            if api_key == "YOUR_API_KEY" or len(api_key) < 10:
                print_error("API_KEY appears to be a placeholder or invalid")
                print_info("Update with your actual Azure OpenAI API key")

        # Check for environment variables
        print(f"\n{Colors.BOLD}Environment Variables:{Colors.END}")
        has_env_vars = False
        for key, value in host_agent.items():
            if isinstance(value, str) and ("${" in value or "%" in value):
                has_env_vars = True
                print_success(f"{key} uses environment variables")

        if not has_env_vars:
            print_warning("No environment variables detected in configuration")
            print_info("Consider using environment variables for API keys and endpoints")
            print_info("Example: API_KEY: ${AZURE_OPENAI_API_KEY}")

        # Check for model configurations
        print(f"\n{Colors.BOLD}Model Configurations:{Colors.END}")
        if "MODELS" in config:
            print_success("MODELS section found in configuration")
        else:
            print_warning("No MODELS section found in configuration")

        # Summary
        print(f"\n{Colors.BOLD}Configuration Summary:{Colors.END}")
        print_success("Configuration file is valid")
        return True

    except ImportError:
        print_error("Failed to import yaml module")
        print_info("Run: pip install pyyaml")
        return False
    except Exception as e:
        print_error(f"Error validating config: {str(e)}")
        traceback.print_exc()
        return False


def test_ufo_imports():
    """Test importing the UFO modules."""
    print_header("UFO Import Test")    modules = [
        ("ufo", "Core UFO module"),
        ("ufo.ufo", "Main UFO class"),
        ("ufo.llm", "LLM module"),
        ("ufo.llm.openai", "OpenAI LLM implementation"),
        ("ufo.utils", "Utilities module"),
        ("ufo.prompter", "Prompter module")
    ]

    all_ok = True
    for module, description in modules:
        try:
            importlib.import_module(module)
            print_success(f"Successfully imported {module} ({description})")
        except Exception as e:
            all_ok = False
            print_error(f"Failed to import {module}: {str(e)}")

    # Summary
    print(f"\n{Colors.BOLD}Import Test Summary:{Colors.END}")
    if all_ok:
        print_success("All UFO modules imported successfully.")
        return True
    else:
        print_error("Some UFO modules could not be imported.")
        return False


def test_api_connectivity():
    """Test API connectivity."""
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
            config = yaml.safe_load(f)        host_agent = config["HOST_AGENT"]
        api_type = host_agent["API_TYPE"].lower()        if api_type == "azure" or api_type == "aoai":
            print_info("Testing Azure OpenAI API connection...")
            api_base = host_agent["API_BASE"]
            api_key = host_agent["API_KEY"]
            api_deployment = host_agent["API_DEPLOYMENT_ID"]
            api_version = host_agent.get("API_VERSION", "2024-05-01")

            try:
                from openai import AzureOpenAI

                client = AzureOpenAI(
                    azure_endpoint=api_base,
                    api_key=api_key,
                    api_version=api_version
                )
                
                response = client.chat.completions.create(
                    model=api_deployment,
                    messages=[{"role": "user", "content": "Say hello"}],
                    max_tokens=10
                )
                
                print_success("Successfully connected to Azure OpenAI API")
                print_info(f"Response: {response.choices[0].message.content}")
                
            except Exception as e:
                print_error(f"Azure OpenAI API test failed: {str(e)}")
                
                # Check for common errors and provide guidance
                error_str = str(e).lower()
                if "not found" in error_str or "unavailable_model" in error_str:
                    print_warning("The deployment name in your config doesn't match any deployment in your Azure OpenAI resource")
                    print_info(f"Current deployment ID: {api_deployment}")
                    print_info("Check Azure Portal for your actual deployment names")
                
                return False
                
        elif api_type == "openai":
            print_info("Testing OpenAI API connection...")
            api_key = host_agent["API_KEY"]
            
            try:
                from openai import OpenAI
                
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": "Say hello"}],
                    max_tokens=10
                )
                
                print_success("Successfully connected to OpenAI API")
                print_info(f"Response: {response.choices[0].message.content}")
                
            except Exception as e:
                print_error(f"OpenAI API test failed: {str(e)}")
                return False
                
        else:
            print_warning(f"API type '{api_type}' testing not supported")
            print_info("Only 'azure' and 'openai' API types are supported for testing")
            return True

        # Test UFO LLM wrapper
        print(f"\n{Colors.BOLD}Testing UFO LLM wrapper:{Colors.END}")
        try:
            from ufo.llm import llm_manager
            llm = llm_manager.LLMManager()
            
            print_info("Making a test request through UFO...")
            response = llm.ask("What are you?", stream=False)
            
            print_success("UFO LLM wrapper test successful")
            print_info(f"Response preview: {response[:100]}...")
            
            return True
            
        except Exception as e:
            print_error(f"UFO LLM wrapper test failed: {str(e)}")
            traceback.print_exc()
            return False

    except ImportError as e:
        print_error(f"Import error during API test: {str(e)}")
        print_info("Make sure all required packages are installed")
        return False
    except Exception as e:
        print_error(f"Error during API test: {str(e)}")
        traceback.print_exc()
        return False


def check_vs_code_setup():
    """Check VS Code setup."""
    print_header("VS Code Setup Check")

    project_root = Path(__file__).parent
    vscode_dir = project_root / ".vscode"

    if not vscode_dir.is_dir():
        print_warning(".vscode directory not found")
        print_info("VS Code configuration has not been set up")
        return False

    # Check for key VS Code config files
    config_files = {
        "launch.json": "VS Code debugging configuration",
        "settings.json": "VS Code workspace settings", 
        "extensions.json": "VS Code recommended extensions"
    }

    all_ok = True
    for filename, description in config_files.items():
        file_path = vscode_dir / filename
        if file_path.exists():
            print_success(f"{filename} exists ({description})")
        else:
            print_warning(f"Missing {filename} ({description})")
            all_ok = False

    # Summary
    print(f"\n{Colors.BOLD}VS Code Setup Summary:{Colors.END}")
    if all_ok:
        print_success("VS Code is properly set up for UFO development")
    else:
        print_warning("VS Code setup is incomplete")
        print_info("Run the installation script again or set up .vscode manually")

    return all_ok


def main():
    """Run all validation tests."""
    print(f"{Colors.BOLD}{Colors.MAGENTA}UFO² COMPREHENSIVE VALIDATION{Colors.END}")
    print(f"{Colors.MAGENTA}{'=' * 60}{Colors.END}")
    print(f"{Colors.CYAN}Date: {Colors.END}{Colors.BOLD}{Colors.CYAN}2025-05-25{Colors.END}")
    print(f"{Colors.CYAN}Python: {Colors.END}{Colors.BOLD}{Colors.CYAN}{sys.version.split()[0]}{Colors.END}")
    print(f"{Colors.MAGENTA}{'=' * 60}{Colors.END}\n")

    # Run tests
    dep_check = check_all_dependencies()
    structure_check = check_ufo_structure()
    config_check = validate_config()
    import_check = test_ufo_imports()
    vscode_check = check_vs_code_setup()
    api_check = test_api_connectivity()

    # Final summary
    print_header("Final Summary")
    
    tests = [
        ("Dependencies", dep_check),
        ("UFO Structure", structure_check),
        ("Configuration", config_check),
        ("Imports", import_check),
        ("VS Code Setup", vscode_check),
        ("API Connectivity", api_check)
    ]
    
    for name, result in tests:
        if result:
            print_success(f"{name}: PASS")
        else:
            print_error(f"{name}: FAIL")
    
    all_ok = all(result for _, result in tests)
    
    if all_ok:
        print(f"\n{Colors.BOLD}{Colors.GREEN}UFO² VALIDATION SUCCESSFUL! 🎉{Colors.END}")
        print_success("Your UFO² installation appears to be correctly set up.")
        print_info("You're ready to start using UFO²!")
        return 0
    else:
        print(f"\n{Colors.BOLD}{Colors.YELLOW}UFO² VALIDATION PARTIALLY SUCCESSFUL{Colors.END}")
        print_warning("Some checks failed. Review the output above for details.")
        print_info("Fix the issues and run this script again to verify.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
