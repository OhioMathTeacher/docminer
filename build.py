# Build script for creating ResearchBuddy3.1 executables
# Usage: python build.py [platform]
# Platforms: linux, windows, macos, all

import subprocess
import sys
import platform
import shutil
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors gracefully"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Command: {cmd}")
        print(f"   Error: {e.stderr}")
        return False

def check_dependencies():
    """Check if required build tools are installed"""
    print("🔍 Checking build dependencies...")
    
    deps = [
        ("python", "python3 --version"),
        ("pip", "pip --version"), 
        ("pyinstaller", "python3 -m PyInstaller --version")
    ]
    
    missing = []
    for name, cmd in deps:
        if not run_command(cmd, f"Checking {name}"):
            missing.append(name)
    
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("📦 Install with: pip install pyinstaller")
        return False
    
    return True

def build_executable(target_platform=None):
    """Build executable for specified platform"""
    if not target_platform:
        target_platform = platform.system().lower()
    
    print(f"🔨 Building Research Buddy 3.1 for {target_platform}...")
    
    # Base PyInstaller command
    base_cmd = [
        "python3", "-m", "PyInstaller",
        "--onefile",
        "--windowed", 
        "--distpath", "./dist",
        "--workpath", "./build",
        "--specpath", "./build"
    ]
    
    # Platform-specific settings
    if target_platform == "macos":
        cmd = base_cmd + [
            "--target-arch", "universal2",
            "--name", "ResearchBuddy3.1",
            "--osx-bundle-identifier", "edu.university.researchbuddy",
            "enhanced_training_interface.py"
        ]
    elif target_platform == "windows":
        cmd = base_cmd + [
            "--name", "ResearchBuddy3.1.exe",
            # "--icon", "app.ico",  # Add if you have an icon
            "enhanced_training_interface.py"
        ]
    else:  # linux
        cmd = base_cmd + [
            "--name", "ResearchBuddy3.1",
            "enhanced_training_interface.py"
        ]
    
    # Run PyInstaller
    cmd_str = " ".join(cmd)
    if run_command(cmd_str, f"Building {target_platform} executable"):
        print(f"🎉 Build completed for {target_platform}")
        
        # Show result
        dist_path = Path("./dist")
        if dist_path.exists():
            print(f"📦 Executable created in: {dist_path.absolute()}")
            for exe in dist_path.glob("*"):
                print(f"   📄 {exe.name} ({exe.stat().st_size // 1024} KB)")
        
        return True
    else:
        print(f"❌ Build failed for {target_platform}")
        return False

def create_distribution_package(target_platform=None):
    """Create distribution package with documentation"""
    if not target_platform:
        target_platform = platform.system().lower()
    
    print(f"📦 Creating distribution package for {target_platform}...")
    
    # Create distribution directory
    dist_dir = Path("./distribution")
    dist_dir.mkdir(exist_ok=True)
    
    platform_dir = dist_dir / f"ResearchBuddy3.1-{target_platform}"
    platform_dir.mkdir(exist_ok=True)
    
    # Copy executable
    dist_path = Path("./dist")
    for exe in dist_path.glob("*"):
        if exe.is_file():
            shutil.copy2(exe, platform_dir)
            print(f"   ✅ Copied {exe.name}")
    
    # Copy documentation
    docs = [
        "README.md",
        "QUICK_REFERENCE.md", 
        "GA_TRAINING_GUIDE_3.0.md",
        "requirements.txt"
    ]
    
    for doc in docs:
        if Path(doc).exists():
            shutil.copy2(doc, platform_dir)
            print(f"   ✅ Copied {doc}")
    
    # Create archive
    if target_platform == "windows":
        archive_name = f"ResearchBuddy3.0-{target_platform}"
        shutil.make_archive(str(dist_dir / archive_name), 'zip', platform_dir)
        print(f"   📦 Created {archive_name}.zip")
    else:
        archive_name = f"ResearchBuddy3.0-{target_platform}"
        shutil.make_archive(str(dist_dir / archive_name), 'gztar', platform_dir)
        print(f"   📦 Created {archive_name}.tar.gz")
    
    return True

def main():
    """Main build script"""
    target = sys.argv[1] if len(sys.argv) > 1 else None
    current_platform = platform.system().lower()
    
    print("🚀 Research Buddy 3.1 Build Script")
    print(f"   Current platform: {current_platform}")
    print(f"   Target platform: {target or current_platform}")
    print()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Determine what to build
    if target == "all":
        print("⚠️  Cross-platform builds require GitHub Actions")
        print("   Building for current platform only...")
        target = current_platform
    elif target and target != current_platform:
        print(f"⚠️  Cross-platform build requested ({target})")
        print(f"   Current platform is {current_platform}")
        print("   For reliable cross-platform builds, use GitHub Actions")
        print("   Continuing with current platform...")
        target = current_platform
    
    target = target or current_platform
    
    # Build executable
    if build_executable(target):
        create_distribution_package(target)
        
        print()
        print("🎉 Build completed successfully!")
        print("📁 Check the ./distribution/ folder for your executable")
        print()
        print("🚀 Next steps:")
        print("   1. Test the executable on your target platform")
        print("   2. Create a GitHub release for distribution") 
        print("   3. Share with your GA team!")
        
    else:
        print("❌ Build failed. Check error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()