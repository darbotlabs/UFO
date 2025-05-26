#!/usr/bin/env python3
"""
UFO² Mission Test Script
This script validates the UFO installation and configuration.
"""

import sys
import os
import subprocess
from pathlib import Path

def test_ufo_import():
    """Test if UFO can be imported successfully."""
    print("🧪 Testing UFO import...")
    try:
        # Add UFO directory to Python path
        ufo_path = Path(__file__).parent
        sys.path.insert(0, str(ufo_path))
        
        # Try importing UFO modules
        import ufo
        print("✅ UFO module imported successfully")
        return True
    except ImportError as e:
        print(f"❌ UFO import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during import: {e}")
        return False

def test_config_file():
    """Test if config.yaml exists and is readable."""
    print("\n🧪 Testing configuration file...")
    config_path = Path(__file__).parent / "ufo" / "config" / "config.yaml"
    
    if not config_path.exists():
        print(f"❌ Config file not found at {config_path}")
        return False
    
    try:
        with open(config_path, 'r') as f:
            content = f.read()
            if "AZURE_OPENAI_API_BASE" in content and "AZURE_OPENAI_API_KEY" in content:
                print("✅ Configuration file exists and contains Azure OpenAI settings")
                return True
            else:
                print("⚠️ Configuration file exists but may be missing required settings")
                return False
    except Exception as e:
        print(f"❌ Error reading config file: {e}")
        return False

def test_virtual_environment():
    """Test if we're running in the correct virtual environment."""
    print("\n🧪 Testing virtual environment...")
    python_path = sys.executable
    
    if "ufo_env" in python_path:
        print(f"✅ Running in UFO virtual environment: {python_path}")
        return True
    else:
        print(f"⚠️ Not running in UFO virtual environment. Current path: {python_path}")
        return False

def test_required_packages():
    """Test if required packages are installed."""
    print("\n🧪 Testing required packages...")
    required_packages = [
        "pandas",
        "azure-identity", 
        "faiss-cpu",
        "sentence-transformers",
        "langchain-huggingface",
        "lxml",
        "opencv-python",
        "pyautogui"
    ]
    
    failed_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            failed_packages.append(package)
    
    if not failed_packages:
        print("✅ All required packages are installed")
        return True
    else:
        print(f"⚠️ Missing packages: {', '.join(failed_packages)}")
        return False

def test_ufo_cli():
    """Test UFO CLI functionality."""
    print("\n🧪 Testing UFO CLI...")
    try:
        # Test UFO CLI with help command
        result = subprocess.run([sys.executable, "-m", "ufo", "--help"], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ UFO CLI is working")
            return True
        else:
            print(f"❌ UFO CLI failed with return code {result.returncode}")
            print(f"Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ UFO CLI test timed out")
        return False
    except Exception as e:
        print(f"❌ UFO CLI test failed: {e}")
        return False

def main():
    """Run all tests and provide summary."""
    print("🛸 UFO² Mission Test Suite")
    print("=" * 50)
    
    tests = [
        test_virtual_environment,
        test_required_packages,
        test_config_file,
        test_ufo_import,
        test_ufo_cli
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 50)
    print("🛸 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {passed/total*100:.1f}%")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! UFO² is ready for operation.")
        return 0
    elif passed >= total * 0.8:
        print("\n✅ MOSTLY WORKING! UFO² should be functional with minor issues.")
        return 0
    else:
        print("\n⚠️ ISSUES DETECTED! Please review failed tests above.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)