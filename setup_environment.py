#!/usr/bin/env python3
"""
Environment Variable Setup Script for Research Buddy

This script helps users set up the required environment variables
for secure credential management.
"""

import os
import sys
from pathlib import Path


def detect_shell():
    """Detect the user's shell and return appropriate config file"""
    shell = os.environ.get('SHELL', '')
    
    if 'zsh' in shell:
        return Path.home() / '.zshrc'
    elif 'bash' in shell:
        return Path.home() / '.bashrc'
    elif 'fish' in shell:
        return Path.home() / '.config' / 'fish' / 'config.fish'
    else:
        # Default to .bashrc
        return Path.home() / '.bashrc'


def add_environment_variables(api_key, github_token):
    """Add environment variables to the shell configuration file"""
    config_file = detect_shell()
    
    # Create the lines to add
    lines_to_add = [
        "\n# Research Buddy Configuration",
        f"export RESEARCH_BUDDY_OPENAI_API_KEY=\"{api_key}\"",
        f"export RESEARCH_BUDDY_GITHUB_TOKEN=\"{github_token}\"",
        ""
    ]
    
    try:
        # Read existing content
        existing_content = ""
        if config_file.exists():
            with open(config_file, 'r') as f:
                existing_content = f.read()
        
        # Check if variables already exist
        if "RESEARCH_BUDDY_OPENAI_API_KEY" in existing_content:
            print(f"⚠️  RESEARCH_BUDDY_OPENAI_API_KEY already exists in {config_file}")
            print("You may need to update it manually.")
            return False
            
        # Append the new environment variables
        with open(config_file, 'a') as f:
            f.write('\n'.join(lines_to_add))
            
        print(f"✅ Environment variables added to {config_file}")
        print("\n🔄 To apply changes, run:")
        print(f"   source {config_file}")
        print("   or restart your terminal")
        
        return True
        
    except Exception as e:
        print(f"❌ Error writing to {config_file}: {e}")
        return False


def check_existing_variables():
    """Check if environment variables are already set"""
    api_key = os.environ.get("RESEARCH_BUDDY_OPENAI_API_KEY", "")
    github_token = os.environ.get("RESEARCH_BUDDY_GITHUB_TOKEN", "")
    
    print("🔍 Checking existing environment variables...")
    
    if api_key:
        print(f"✅ RESEARCH_BUDDY_OPENAI_API_KEY is set ({api_key[:8]}...)")
    else:
        print("❌ RESEARCH_BUDDY_OPENAI_API_KEY is not set")
        
    if github_token:
        print(f"✅ RESEARCH_BUDDY_GITHUB_TOKEN is set ({github_token[:8]}...)")
    else:
        print("❌ RESEARCH_BUDDY_GITHUB_TOKEN is not set")
        
    return bool(api_key and github_token)


def main():
    """Main setup function"""
    print("🔧 Research Buddy Environment Variable Setup")
    print("=" * 50)
    
    # Check existing variables first
    if check_existing_variables():
        print("\n✅ All environment variables are already set!")
        print("You can run Research Buddy now.")
        return
    
    print("\n📝 Setting up environment variables for secure credential storage...")
    print("\nThis script will add environment variables to your shell configuration.")
    print("Your credentials will NOT be stored in plain text files.")
    
    # Get API key
    print("\n🔑 OpenAI API Key Setup:")
    api_key = input("Enter your OpenAI API key (starts with 'sk-'): ").strip()
    
    if not api_key.startswith('sk-'):
        print("❌ Invalid OpenAI API key. It should start with 'sk-'")
        return
    
    # Get GitHub token
    print("\n🔑 GitHub Token Setup:")
    print("Generate a token at: https://github.com/settings/tokens")
    print("Required permissions: 'repo' (for uploading to repositories)")
    github_token = input("Enter your GitHub token (starts with 'ghp_' or 'github_pat_'): ").strip()
    
    if not github_token.startswith(('ghp_', 'github_pat_')):
        print("❌ Invalid GitHub token. It should start with 'ghp_' or 'github_pat_'")
        return
    
    # Add to shell configuration
    print(f"\n📁 Detected shell configuration: {detect_shell()}")
    
    confirm = input("\nAdd these environment variables to your shell configuration? (y/N): ").strip().lower()
    if confirm in ['y', 'yes']:
        if add_environment_variables(api_key, github_token):
            print("\n🎉 Setup complete!")
            print("\nNext steps:")
            print("1. Restart your terminal or run: source ~/.zshrc (or your shell config)")
            print("2. Run the Research Buddy configuration dialog to set repository settings")
            print("3. Start using Research Buddy!")
        else:
            print("\n❌ Setup failed. You can manually add these lines to your shell config:")
            print(f"export RESEARCH_BUDDY_OPENAI_API_KEY=\"{api_key}\"")
            print(f"export RESEARCH_BUDDY_GITHUB_TOKEN=\"{github_token}\"")
    else:
        print("\n📋 Manual setup instructions:")
        print("Add these lines to your shell configuration file (~/.zshrc, ~/.bashrc, etc.):")
        print(f"export RESEARCH_BUDDY_OPENAI_API_KEY=\"{api_key}\"")
        print(f"export RESEARCH_BUDDY_GITHUB_TOKEN=\"{github_token}\"")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")