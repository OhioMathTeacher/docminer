#!/usr/bin/env python3
"""
Simple test script to verify OpenAI API connection
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

def test_openai_connection():
    """Test OpenAI API connection"""
    print("🔍 Testing OpenAI API Connection...")
    
    # Try to get API key from environment
    api_key = os.environ.get("RESEARCH_BUDDY_OPENAI_API_KEY", "")
    
    if not api_key:
        print("❌ OpenAI API key not found in environment variables")
        
        # Try loading from config file
        try:
            from configuration_dialog import load_configuration
            config = load_configuration()
            print(f"📁 Config loaded: {bool(config)}")
            
            # Check if we can get the API key through the config system
            if config:
                print("✅ Configuration system is working")
            else:
                print("❌ Configuration system failed")
                
        except Exception as e:
            print(f"❌ Error loading configuration: {e}")
            return False
    else:
        print(f"✅ OpenAI API key found (length: {len(api_key)} chars)")
    
    # Test actual API call
    try:
        import openai
        
        # Set the API key
        if api_key:
            openai.api_key = api_key
        else:
            print("❌ No API key available for testing")
            return False
            
        print("🚀 Making test API call...")
        
        # Make a simple API call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Say 'Hello from Research Buddy!' in exactly those words."}
            ],
            max_tokens=50
        )
        
        reply = response.choices[0].message.content.strip()
        print(f"✅ API Response: {reply}")
        
        if "Hello from Research Buddy!" in reply:
            print("🎉 OpenAI API connection is working perfectly!")
            return True
        else:
            print("⚠️  API responded but with unexpected content")
            return True
            
    except Exception as e:
        print(f"❌ API call failed: {e}")
        return False

def test_github_connection():
    """Test GitHub API connection"""
    print("\n🔍 Testing GitHub API Connection...")
    
    # Try to get GitHub token from environment
    github_token = os.environ.get("RESEARCH_BUDDY_GITHUB_TOKEN", "")
    
    if not github_token:
        print("❌ GitHub token not found in environment variables")
        return False
    else:
        print(f"✅ GitHub token found (length: {len(github_token)} chars)")
    
    # Test GitHub API call
    try:
        import requests
        
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        print("🚀 Making test GitHub API call...")
        response = requests.get("https://api.github.com/user", headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            username = user_data.get("login", "Unknown")
            print(f"✅ GitHub API working! Authenticated as: {username}")
            return True
        else:
            print(f"❌ GitHub API call failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ GitHub API call failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Research Buddy API Connection Test")
    print("=" * 50)
    
    openai_ok = test_openai_connection()
    github_ok = test_github_connection()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"OpenAI API: {'✅ Working' if openai_ok else '❌ Failed'}")
    print(f"GitHub API: {'✅ Working' if github_ok else '❌ Failed'}")
    
    if openai_ok and github_ok:
        print("\n🎉 All systems go! Research Buddy is ready to use!")
    else:
        print("\n⚠️  Some connections failed. Check your API keys and try running the setup again.")