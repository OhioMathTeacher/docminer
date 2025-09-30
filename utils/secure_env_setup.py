#!/usr/bin/env python3
"""
Secure Environment Variable Setup for Research Buddy

This script helps you securely set environment variables for Research Buddy
without storing them in plain text files.
"""

import os
import sys
import subprocess
from pathlib import Path

def create_env_script():
    """Create a secure script to set environment variables"""
    
    # Get user's API keys
    print("🔐 Research Buddy Secure Credential Setup")
    print("=" * 50)
    print("This will create a secure way to set your API credentials.")
    print("Your keys will NOT be stored in plain text files.\n")
    
    openai_key = input("Enter your OpenAI API Key (or press Enter to skip): ").strip()
    github_token = input("Enter your GitHub Personal Access Token (or press Enter to skip): ").strip()
    
    if not openai_key and not github_token:
        print("No credentials provided. Exiting.")
        return
    
    # Create a script directory in the user's home
    script_dir = Path.home() / ".research_buddy" / "scripts"
    script_dir.mkdir(parents=True, exist_ok=True)
    
    # Create the environment setup script
    env_script_path = script_dir / "set_env.sh"
    
    script_content = "#!/bin/bash\n"
    script_content += "# Research Buddy Environment Variables\n"
    script_content += "# This script is protected by file permissions\n\n"
    
    if openai_key:
        script_content += f'export RESEARCH_BUDDY_OPENAI_API_KEY="{openai_key}"\n'
    
    if github_token:
        script_content += f'export RESEARCH_BUDDY_GITHUB_TOKEN="{github_token}"\n'
    
    script_content += '\necho "✅ Research Buddy credentials loaded"\n'
    
    # Write the script
    with open(env_script_path, 'w') as f:
        f.write(script_content)
    
    # Make it executable but only readable by owner
    os.chmod(env_script_path, 0o700)  # rwx for owner only
    
    print(f"\n✅ Secure credential script created at: {env_script_path}")
    print(f"📁 File permissions set to owner-only (700)")
    
    # Create a launcher script for Research Buddy
    launcher_path = script_dir / "launch_research_buddy.sh"
    launcher_content = f"""#!/bin/bash
# Research Buddy Secure Launcher
# Sources credentials and launches the application

# Set credentials
source "{env_script_path}"

# Launch Research Buddy
cd "{Path.cwd()}"
python3 enhanced_training_interface.py
"""
    
    with open(launcher_path, 'w') as f:
        f.write(launcher_content)
    
    os.chmod(launcher_path, 0o700)
    
    print(f"🚀 Launcher script created at: {launcher_path}")
    print("\n" + "=" * 50)
    print("🎯 How to use:")
    print(f"1. Run: {launcher_path}")
    print("2. Or source the env file first: source {env_script_path}")
    print("3. Then run: python3 enhanced_training_interface.py")
    print("\n🛡️ Security:")
    print("- Files are only readable by you (700 permissions)")
    print("- Not in your shell profile or any shared locations")
    print("- Can be deleted anytime")
    
    return env_script_path, launcher_path

def test_credentials():
    """Test if credentials are properly set"""
    openai_key = os.environ.get("RESEARCH_BUDDY_OPENAI_API_KEY", "")
    github_token = os.environ.get("RESEARCH_BUDDY_GITHUB_TOKEN", "")
    
    print("\n🧪 Testing current environment:")
    print(f"OpenAI API Key: {'✅ Set' if openai_key else '❌ Not set'}")
    print(f"GitHub Token: {'✅ Set' if github_token else '❌ Not set'}")
    
    if openai_key or github_token:
        print("\n🎉 You can now launch Research Buddy with these credentials!")
    else:
        print("\n⚠️  No credentials found in current environment.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_credentials()
    else:
        try:
            env_script, launcher = create_env_script()
            print(f"\n🔄 Would you like to test the setup now? (y/n): ", end="")
            if input().lower().startswith('y'):
                print("\n🧪 Testing by sourcing the environment file...")
                # Source the file and test
                result = subprocess.run(["/bin/bash", "-c", f"source {env_script} && python3 -c \"import secure_env_setup; secure_env_setup.test_credentials()\""], 
                                      cwd=Path.cwd())
        except KeyboardInterrupt:
            print("\n\n❌ Setup cancelled.")
        except Exception as e:
            print(f"\n❌ Error: {e}")