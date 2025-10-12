#!/usr/bin/env python3
"""
DocMiner Rebrand Script
Automatically rebrand Research Buddy to DocMiner across the entire codebase.
"""

import os
import re
import shutil
import argparse
from pathlib import Path
from typing import List, Tuple, Dict

# Replacement mappings (order matters - most specific first)
REPLACEMENTS = [
    # URLs and GitHub references
    (r'research-buddy', 'docminer'),
    (r'Research-Buddy', 'DocMiner'),
    
    # Executable/file names (no space)
    (r'ResearchBuddy', 'DocMiner'),
    
    # UI text and documentation (with space)
    (r'Research Buddy', 'DocMiner'),
    
    # All lowercase variants
    (r'researchbuddy', 'docminer'),
]

# Files/directories to skip
SKIP_PATTERNS = [
    'rebrand/',           # This directory
    '.git/',              # Git metadata
    '__pycache__/',       # Python cache
    '*.pyc',              # Compiled Python
    'archive/',           # Historical files
    'training_reports/',  # Historical training data
    'batch_reports/',     # Historical batch data
    'venv*/',             # Virtual environments
    'AppDir/',            # Temporary build directory
    'dist/',              # Build outputs
    'build/',             # Build intermediates
    '*.AppImage',         # Binary files
    '*.dmg',              # Binary files
    '*.exe',              # Binary files
    '*.zip',              # Archives
    '*.tar.gz',           # Archives
]

# Files to rename (old_name -> new_name)
FILE_RENAMES = {
    'start_research_buddy.sh': 'start_docminer.sh',
    'test_config.sh': 'test_config.sh',  # Keep as-is
    'simulate_fresh_user.sh': 'simulate_fresh_user.sh',  # Keep as-is
    'run_research_buddy.py': 'run_docminer.py',
    'launch_research_buddy.py': 'launch_docminer.py',
    'build_files/ResearchBuddy5.2.spec': 'build_files/DocMiner5.2.spec',
    'build_files/ResearchBuddy5.0.spec': 'build_files/DocMiner5.0.spec',
    'build_files/ResearchBuddy4.0.spec': 'build_files/DocMiner4.0.spec',
    'build_files/ResearchBuddy4.1.spec': 'build_files/DocMiner4.1.spec',
    'build_files/ResearchBuddy4.2.spec': 'build_files/DocMiner4.2.spec',
    'build_files/ResearchBuddy3.1.2.spec': 'build_files/DocMiner3.1.2.spec',
    'ResearchBuddy.spec': 'DocMiner.spec',
}

class Rebrander:
    def __init__(self, root_dir: Path, preview: bool = True):
        self.root_dir = root_dir
        self.preview = preview
        self.changes: List[Tuple[str, str, str]] = []
        self.file_renames: List[Tuple[Path, Path]] = []
        
    def should_skip(self, path: Path) -> bool:
        """Check if a path should be skipped"""
        path_str = str(path.relative_to(self.root_dir))
        
        for pattern in SKIP_PATTERNS:
            if pattern.endswith('/'):
                if path_str.startswith(pattern.rstrip('/')):
                    return True
            elif '*' in pattern:
                import fnmatch
                if fnmatch.fnmatch(path_str, pattern):
                    return True
            elif pattern in path_str:
                return True
        
        return False
    
    def is_text_file(self, path: Path) -> bool:
        """Check if file is likely a text file"""
        text_extensions = {
            '.py', '.md', '.txt', '.sh', '.yml', '.yaml', '.json',
            '.spec', '.desktop', '.command', '.rst', '.cfg', '.ini'
        }
        
        if path.suffix.lower() in text_extensions:
            return True
        
        # Check if file has no extension and might be a script
        if not path.suffix and path.is_file():
            try:
                with open(path, 'rb') as f:
                    chunk = f.read(512)
                    return b'\0' not in chunk  # No null bytes = probably text
            except:
                return False
        
        return False
    
    def replace_in_file(self, file_path: Path):
        """Replace text in a single file"""
        if not self.is_text_file(file_path):
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (UnicodeDecodeError, PermissionError):
            return
        
        original_content = content
        
        # Apply all replacements
        for old_pattern, new_text in REPLACEMENTS:
            content = re.sub(old_pattern, new_text, content)
        
        if content != original_content:
            relative_path = file_path.relative_to(self.root_dir)
            
            # Count changes
            changes_count = sum(1 for old, new in REPLACEMENTS 
                              if old in original_content or re.search(old, original_content))
            
            self.changes.append((str(relative_path), original_content, content))
            
            if not self.preview:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  ✅ Updated: {relative_path} ({changes_count} replacements)")
            else:
                print(f"  📝 Would update: {relative_path} ({changes_count} replacements)")
    
    def rename_files(self):
        """Rename files according to FILE_RENAMES mapping"""
        for old_name, new_name in FILE_RENAMES.items():
            old_path = self.root_dir / old_name
            new_path = self.root_dir / new_name
            
            if old_path.exists():
                self.file_renames.append((old_path, new_path))
                
                if not self.preview:
                    old_path.rename(new_path)
                    print(f"  ✅ Renamed: {old_name} → {new_name}")
                else:
                    print(f"  📝 Would rename: {old_name} → {new_name}")
    
    def process_directory(self, directory: Path):
        """Recursively process all files in directory"""
        for item in directory.rglob('*'):
            if self.should_skip(item):
                continue
            
            if item.is_file():
                self.replace_in_file(item)
    
    def create_backup(self):
        """Create a backup before making changes"""
        if self.preview:
            return
        
        backup_dir = self.root_dir.parent / f"{self.root_dir.name}_backup_before_rebrand"
        
        if backup_dir.exists():
            print(f"\n⚠️  Backup already exists: {backup_dir}")
            response = input("Overwrite? (y/n): ")
            if response.lower() != 'y':
                print("❌ Aborted")
                exit(1)
            shutil.rmtree(backup_dir)
        
        print(f"💾 Creating backup: {backup_dir}")
        shutil.copytree(self.root_dir, backup_dir, 
                       ignore=shutil.ignore_patterns(
                           '__pycache__', '*.pyc', '.git', 'venv*', 
                           'dist', 'build', 'AppDir', '*.AppImage'
                       ))
        print(f"✅ Backup created\n")
    
    def show_summary(self):
        """Show summary of changes"""
        print("\n" + "="*60)
        print("📊 REBRAND SUMMARY")
        print("="*60)
        print(f"Files to modify: {len(self.changes)}")
        print(f"Files to rename: {len(self.file_renames)}")
        
        if self.preview:
            print("\n🔍 PREVIEW MODE - No changes were made")
            print("Run with --execute to apply changes")
        else:
            print("\n✅ CHANGES APPLIED")
            print("\nNext steps:")
            print("1. Test the application locally")
            print("2. Review changes: git diff")
            print("3. Commit: git add . && git commit -m 'Rebrand to DocMiner'")
            print("4. Rename GitHub repo: Settings → Repository name → 'docminer'")
            print("5. Update remote: git remote set-url origin https://github.com/OhioMathTeacher/docminer.git")
    
    def run(self):
        """Execute the rebrand process"""
        print("🎨 DocMiner Rebrand Script")
        print("="*60)
        
        if not self.preview:
            print("⚠️  WARNING: This will modify files!")
            response = input("Continue? (yes/no): ")
            if response.lower() != 'yes':
                print("❌ Aborted")
                return
            
            self.create_backup()
        
        print("\n📝 Processing text replacements...")
        self.process_directory(self.root_dir)
        
        print("\n📁 Processing file renames...")
        self.rename_files()
        
        self.show_summary()


def main():
    parser = argparse.ArgumentParser(
        description='Rebrand Research Buddy to DocMiner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python3 rebrand.py --preview   # See what will change (safe)
  python3 rebrand.py --execute   # Apply the rebrand
        '''
    )
    
    parser.add_argument(
        '--preview', 
        action='store_true',
        help='Preview changes without modifying files (default)'
    )
    
    parser.add_argument(
        '--execute',
        action='store_true', 
        help='Actually apply the changes'
    )
    
    args = parser.parse_args()
    
    # Default to preview mode
    preview = not args.execute
    
    # Get root directory (parent of rebrand directory)
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    
    rebrander = Rebrander(root_dir, preview=preview)
    rebrander.run()


if __name__ == '__main__':
    main()
