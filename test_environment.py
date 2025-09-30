#!/usr/bin/env python3
"""
Test Environment Variable Configuration for Research Buddy

This script tests the new secure environment variable setup.
"""

import os
from pathlib import Path

def test_environment_variables():
    """Test if environment variables are properly set"""
    print("🔧 Research Buddy Environment Test")
    print("=" * 50)
    
    # Check for environment variables
    openai_key = os.environ.get("RESEARCH_BUDDY_OPENAI_API_KEY", "")
    github_token = os.environ.get("RESEARCH_BUDDY_GITHUB_TOKEN", "")
    
    print("🔍 Checking environment variables...")
    
    if openai_key:
        print(f"✅ RESEARCH_BUDDY_OPENAI_API_KEY: Set ({openai_key[:8]}...)")
    else:
        print("❌ RESEARCH_BUDDY_OPENAI_API_KEY: Not set")
        
    if github_token:
        print(f"✅ RESEARCH_BUDDY_GITHUB_TOKEN: Set ({github_token[:8]}...)")
    else:
        print("❌ RESEARCH_BUDDY_GITHUB_TOKEN: Not set")
    
    print("\n📁 Checking configuration file...")
    
    # Check configuration file
    config_path = Path.home() / ".research_buddy" / "interface_settings.json"
    if config_path.exists():
        print(f"✅ Configuration file exists: {config_path}")
        try:
            import json
            with open(config_path, 'r') as f:
                config = json.load(f)
            print(f"   GitHub Owner: {config.get('github_owner', 'Not set')}")
            print(f"   GitHub Repo: {config.get('github_repo', 'Not set')}")
        except Exception as e:
            print(f"   ❌ Error reading config: {e}")
    else:
        print(f"❌ Configuration file not found: {config_path}")
    
    print("\n📋 Summary:")
    if openai_key and github_token:
        print("✅ Environment variables are configured correctly!")
        if config_path.exists():
            print("✅ Configuration file exists!")
            print("🎉 Research Buddy is ready to use!")
        else:
            print("⚠️  Run the configuration dialog to set repository settings.")
    else:
        print("❌ Environment variables need to be set.")
        print("\n🔧 To set environment variables:")
        print("1. Run: python3 setup_environment.py")
        print("2. Or manually add to your shell config (~/.zshrc, ~/.bashrc):")
        print("   export RESEARCH_BUDDY_OPENAI_API_KEY=\"sk-your-key-here\"")
        print("   export RESEARCH_BUDDY_GITHUB_TOKEN=\"ghp_your-token-here\"")

if __name__ == "__main__":
    test_environment_variables()