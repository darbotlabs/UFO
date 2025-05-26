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
