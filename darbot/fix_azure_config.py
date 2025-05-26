#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
UFO² Azure OpenAI Configuration Helper
Created: 2025-05-25

This script helps fix common Azure OpenAI configuration issues in UFO²,
particularly the "unavailable_model" error.
"""

import os
import sys
import yaml
from pathlib import Path

# ANSI colors for formatting
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
END = "\033[0m"
BOLD = "\033[1m"

def print_header(text):
    """Print a formatted header."""
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

def fix_azure_openai_config():
    """Fix Azure OpenAI configuration issues."""
    print_header("Azure OpenAI Configuration Helper")
    
    # Find config file
    config_path = Path(__file__).parent / "ufo" / "config" / "config.yaml"
    if not config_path.exists():
        print_error(f"Config file not found at {config_path}")
        return False
    
    # Load config
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print_error(f"Failed to load config: {e}")
        return False
    
    # Check if using Azure OpenAI
    if "HOST_AGENT" not in config:
        print_error("Missing HOST_AGENT section in config")
        return False
    
    host_agent = config["HOST_AGENT"]
    api_type = host_agent.get("API_TYPE", "").lower()
    
    if api_type not in ["azure", "aoai"]:
        print_info("Not using Azure OpenAI. No fixes needed.")
        return True
    
    # Check current configuration
    print_info("Current Azure OpenAI Configuration:")
    
    api_base = host_agent.get("API_BASE", "")
    api_key = host_agent.get("API_KEY", "")
    api_deployment = host_agent.get("API_DEPLOYMENT_ID", "")
    api_model = host_agent.get("API_MODEL", "")
    
    print(f"API_TYPE:          {api_type}")
    print(f"API_BASE:          {api_base}")
    print(f"API_KEY:           {'[REDACTED]' if api_key else '[MISSING]'}")
    print(f"API_DEPLOYMENT_ID: {api_deployment}")
    print(f"API_MODEL:         {api_model}")
    print("")
    
    # Check for common issues
    issues_detected = False
    
    if not api_base or "your" in api_base.lower():
        print_warning("API_BASE is missing or contains placeholder text")
        issues_detected = True
    
    if not api_key or "your" in api_key.lower():
        print_warning("API_KEY is missing or contains placeholder text")
        issues_detected = True
    
    # Check if deployment ID looks like a model name
    common_model_names = ["gpt-4o", "gpt-4", "gpt-35-turbo", "gpt-3.5-turbo"]
    if api_deployment in common_model_names:
        print_warning(f"API_DEPLOYMENT_ID '{api_deployment}' looks like a model name, not a deployment name")
        print_info("In Azure OpenAI, the deployment ID should match your actual deployment name in Azure OpenAI Studio")
        issues_detected = True
    
    if not issues_detected:
        print_success("No common issues detected in your Azure OpenAI configuration")
        return True
    
    # Ask if user wants to fix issues
    print_info("Would you like to update the configuration to fix these issues? (y/n)")
    choice = input().strip().lower()
    
    if choice != 'y':
        print_info("No changes were made to your configuration")
        return False
    
    # Update configuration
    changes_made = False
    
    # Fix API_BASE
    if not api_base or "your" in api_base.lower():
        print_info("Enter your Azure OpenAI endpoint URL (e.g., https://your-resource.openai.azure.com):")
        new_api_base = input().strip()
        
        if new_api_base:
            host_agent["API_BASE"] = new_api_base
            changes_made = True
    
    # Fix API_KEY
    if not api_key or "your" in api_key.lower():
        print_info("Enter your Azure OpenAI API key:")
        new_api_key = input().strip()
        
        if new_api_key:
            host_agent["API_KEY"] = new_api_key
            changes_made = True
    
    # Fix API_DEPLOYMENT_ID
    if api_deployment in common_model_names:
        print_info(f"Current deployment ID '{api_deployment}' looks like a model name")
        print_info("Enter your actual Azure OpenAI deployment name:")
        new_deployment = input().strip()
        
        if new_deployment:
            host_agent["API_DEPLOYMENT_ID"] = new_deployment
            changes_made = True
    
    # Save changes
    if changes_made:
        try:
            # Backup original config
            backup_path = str(config_path) + ".backup"
            with open(backup_path, 'w', encoding='utf-8') as f:
                with open(config_path, 'r', encoding='utf-8') as original:
                    f.write(original.read())
            
            print_success(f"Original configuration backed up to {backup_path}")
            
            # Write updated config
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False)
            
            print_success("Configuration updated successfully")
            return True
        except Exception as e:
            print_error(f"Failed to save configuration: {e}")
            return False
    else:
        print_info("No changes were made to your configuration")
        return False

def main():
    """Main function."""
    print(f"{BOLD}{YELLOW}UFO² AZURE OPENAI CONFIGURATION HELPER{END}")
    print(f"{YELLOW}{'=' * 60}{END}")
    print(f"{CYAN}Date: {END}{BOLD}{CYAN}2025-05-25{END}")
    print(f"{YELLOW}{'=' * 60}{END}\n")
    
    success = fix_azure_openai_config()
    
    if success:
        print_header("Next Steps")
        print_info("Try running a test request with:")
        print("    python -m ufo --request \"Hello, what can you do?\"")
        print("")
        print_info("If you still encounter issues, consider:")
        print("1. Checking your Azure OpenAI Studio for correct deployment names")
        print("2. Using environment variables instead of hardcoded keys")
        print("3. Running the comprehensive validation script:")
        print("    python quick_check.py")
        print("")
        return 0
    else:
        print_header("Configuration Update")
        print_warning("Configuration update was incomplete or unsuccessful")
        print_info("Please manually review your configuration in:")
        print(f"    ufo/config/config.yaml")
        print("")
        return 1

if __name__ == "__main__":
    sys.exit(main())
