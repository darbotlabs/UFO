#!/usr/bin/env python3
"""
UFO² Comprehensive Validation Script
Validates all aspects of the UFO² setup including environment, dependencies, configuration, and functionality.
"""

import os
import sys
import subprocess
import importlib
import yaml
from pathlib import Path

def print_header(title):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"🛸 {title}")
    print('='*60)

def print_test(test_name, status, details=""):
    """Print test result with emoji status."""
    emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
    print(f"{emoji} {test_name}")
    if details:
        print(f"   {details}")

def check_virtual_environment():
    """Check if running in UFO virtual environment."""
    print_header("Virtual Environment Check")
    
    venv_path = os.environ.get('VIRTUAL_ENV', '')
    python_path = sys.executable
    
    if 'ufo_env' in python_path.lower() or 'ufo_env' in venv_path.lower():
        print_test("Virtual Environment", "PASS", f"Running in UFO environment: {python_path}")
        return True
    else:
        print_test("Virtual Environment", "WARN", f"Not in UFO environment: {python_path}")
        return False

def check_python_packages():
    """Check required Python packages."""
    print_header("Python Package Dependencies")
    
    required_packages = [
        'pandas', 'azure-identity', 'faiss-cpu', 'sentence-transformers',
        'langchain-huggingface', 'lxml', 'opencv-python', 'pyautogui',
        'pywinauto', 'openai', 'pyyaml', 'numpy', 'torch'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            importlib.import_module(package.replace('-', '_'))
            print_test(f"Package: {package}", "PASS")
        except ImportError:
            print_test(f"Package: {package}", "FAIL", "Not installed or import failed")
            missing_packages.append(package)
    
    return len(missing_packages) == 0, missing_packages

def check_ufo_installation():
    """Check UFO installation and import."""
    print_header("UFO Installation Check")
    
    try:
        import ufo
        print_test("UFO Module Import", "PASS", f"UFO version: {getattr(ufo, '__version__', 'Unknown')}")
        
        # Check key UFO modules
        modules_to_check = [
            'ufo.agents',
            'ufo.llm',
            'ufo.module'
        ]
        
        for module in modules_to_check:
            try:
                importlib.import_module(module)
                print_test(f"UFO Module: {module}", "PASS")
            except ImportError as e:
                print_test(f"UFO Module: {module}", "FAIL", str(e))
                return False
        
        return True
    except ImportError as e:
        print_test("UFO Module Import", "FAIL", str(e))
        return False

def check_configuration():
    """Check UFO configuration file."""
    print_header("Configuration Check")
    
    config_path = Path("ufo/config/config.yaml")
    
    if not config_path.exists():
        print_test("Config File Exists", "FAIL", f"File not found: {config_path}")
        return False
    
    print_test("Config File Exists", "PASS", f"Found: {config_path}")
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Check required sections
        required_sections = ['HOST_AGENT', 'APP_AGENT', 'BACKUP_AGENT']
        for section in required_sections:
            if section in config:
                agent_config = config[section]
                api_type = agent_config.get('API_TYPE', '')
                api_base = agent_config.get('API_BASE', '')
                api_key = agent_config.get('API_KEY', '')
                api_model = agent_config.get('API_MODEL', '')
                
                print_test(f"{section} Configuration", "PASS" if all([api_type, api_base, api_key, api_model]) else "WARN",
                          f"Type: {api_type}, Model: {api_model}")
            else:
                print_test(f"{section} Configuration", "FAIL", "Section missing")
        
        return True
    except Exception as e:
        print_test("Config File Parse", "FAIL", str(e))
        return False

def check_cli_functionality():
    """Check UFO CLI functionality."""
    print_header("CLI Functionality Check")
    
    try:
        # Test help command
        result = subprocess.run([sys.executable, '-m', 'ufo', '--help'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and 'usage:' in result.stdout:
            print_test("CLI Help Command", "PASS", "Help displays correctly")
        else:
            print_test("CLI Help Command", "FAIL", f"Return code: {result.returncode}")
            return False
        
        # Test basic CLI structure (without making API calls)
        result = subprocess.run([sys.executable, '-c', 
                               "import ufo; print('UFO import successful')"], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print_test("UFO Import Test", "PASS", "UFO imports without errors")
        else:
            print_test("UFO Import Test", "FAIL", result.stderr)
            return False
        
        return True
    except subprocess.TimeoutExpired:
        print_test("CLI Functionality", "FAIL", "Command timeout")
        return False
    except Exception as e:
        print_test("CLI Functionality", "FAIL", str(e))
        return False

def check_directory_structure():
    """Check UFO directory structure."""
    print_header("Directory Structure Check")
    
    required_dirs = [
        'ufo',
        'ufo/config',
        'ufo/agents',
        'ufo/llm',
        'ufo/module',
        'logs'
    ]
    
    all_dirs_exist = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print_test(f"Directory: {dir_path}", "PASS")
        else:
            print_test(f"Directory: {dir_path}", "FAIL", "Directory missing")
            all_dirs_exist = False
    
    return all_dirs_exist

def check_system_requirements():
    """Check system requirements."""
    print_header("System Requirements Check")
    
    # Check Python version
    python_version = sys.version_info
    if python_version >= (3, 8):
        print_test("Python Version", "PASS", f"Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    else:
        print_test("Python Version", "FAIL", f"Python {python_version.major}.{python_version.minor} < 3.8")
        return False
    
    # Check OS
    import platform
    os_name = platform.system()
    if os_name == "Windows":
        print_test("Operating System", "PASS", f"Windows {platform.release()}")
    else:
        print_test("Operating System", "WARN", f"{os_name} (UFO designed for Windows)")
    
    return True

def main():
    """Run comprehensive UFO² validation."""
    print_header("UFO² Comprehensive Validation Suite")
    print("This script validates the complete UFO² setup including:")
    print("• Virtual environment configuration")
    print("• Python package dependencies") 
    print("• UFO installation and modules")
    print("• Configuration files")
    print("• CLI functionality")
    print("• Directory structure")
    print("• System requirements")
    
    test_results = []
    
    # Run all tests
    test_results.append(("Virtual Environment", check_virtual_environment()))
    test_results.append(("Python Packages", check_python_packages()[0]))
    test_results.append(("UFO Installation", check_ufo_installation()))
    test_results.append(("Configuration", check_configuration()))
    test_results.append(("CLI Functionality", check_cli_functionality()))
    test_results.append(("Directory Structure", check_directory_structure()))
    test_results.append(("System Requirements", check_system_requirements()))
    
    # Print summary
    print_header("VALIDATION SUMMARY")
    
    passed_tests = sum(1 for _, result in test_results if result)
    total_tests = len(test_results)
    success_rate = (passed_tests / total_tests) * 100
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🏆 Overall Success Rate: {success_rate:.1f}% ({passed_tests}/{total_tests})")
    
    if success_rate >= 80:
        print("🎉 UFO² setup is ready for operation!")
        return True
    elif success_rate >= 60:
        print("⚠️ UFO² setup has minor issues but may be functional")
        return True
    else:
        print("❌ UFO² setup has significant issues requiring attention")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
