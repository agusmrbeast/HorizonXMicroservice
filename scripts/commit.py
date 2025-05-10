#!/usr/bin/env python3
"""
Unified commit script for the entire project.
Runs linting, formatting, and commitizen across all modules.
"""
import os
import subprocess
import sys
from pathlib import Path

# List of modules to process
MODULES = ["Core", "Academics", "Library"]

def run_command(cmd, cwd=None):
    """Run a command and exit on failure."""
    try:
        subprocess.run(cmd, check=True, cwd=cwd)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {' '.join(cmd)}: {e}")
        return False

def main():
    # Get the root directory (parent of scripts folder)
    root_dir = Path(__file__).parent.parent
    
    # Process each module
    for module in MODULES:
        module_path = root_dir / "src" / module
        if not module_path.exists():
            print(f"⚠️ Module {module} not found, skipping")
            continue
            
        print(f"🔍 Processing {module}...")
        
        # Run lint-fix
        print(f"  Running lint-fix for {module}...")
        if not run_command(["uv", "run", "lint-fix"], cwd=module_path):
            sys.exit(1)
            
        # Run format-fix
        print(f"  Running format-fix for {module}...")
        if not run_command(["uv", "run", "format-fix"], cwd=module_path):
            sys.exit(1)
    
    # Add all changes to git
    print("📝 Adding changes to git...")
    if not run_command(["git", "add", "."], cwd=root_dir):
        sys.exit(1)
    
    # Run commitizen using os.system to avoid terminal compatibility issues
    print("💬 Running commitizen...")
    os.chdir(root_dir)  # Change to root directory
    exit_code = os.system('cz commit')
    if exit_code != 0:
        print("❌ Commitizen failed")
        sys.exit(1)
        
    print("✅ Commit process completed successfully!")

if __name__ == "__main__":
    main()

