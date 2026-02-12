#!/usr/bin/env python3
"""
Release script for BiXFlow package.

This script helps maintainers build and publish BiXFlow packages to PyPI.
"""

import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return its result."""
    print(f"Running: {command}")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            check=True, 
            capture_output=True, 
            text=True
        )
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)

def check_prerequisites():
    """Check if all prerequisites are installed."""
    print("Checking prerequisites...")
    
    # Check if build and twine are installed
    try:
        import build
        import twine
        print("✓ build and twine are installed")
    except ImportError:
        print("✗ build or twine not installed. Installing...")
        run_command("pip install build twine")
    
    # Check if we're in the right directory
    if not Path("setup.py").exists():
        print("✗ setup.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    print("✓ All prerequisites checked")

def clean_previous_builds():
    """Clean previous build artifacts."""
    print("Cleaning previous build artifacts...")
    
    # Remove dist directory if it exists
    dist_dir = Path("dist")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
        print("✓ Removed dist directory")
    
    # Remove build directory if it exists
    build_dir = Path("build")
    if build_dir.exists():
        shutil.rmtree(build_dir)
        print("✓ Removed build directory")
    
    # Remove egg-info directory if it exists
    egg_info_dirs = Path(".").glob("*.egg-info")
    for egg_info_dir in egg_info_dirs:
        shutil.rmtree(egg_info_dir)
        print(f"✓ Removed {egg_info_dir}")

def build_packages():
    """Build source distribution and wheel packages."""
    print("Building packages...")
    
    # Build packages
    run_command("python -m build")
    
    # List built packages
    dist_dir = Path("dist")
    if dist_dir.exists():
        print("Built packages:")
        for file in dist_dir.iterdir():
            print(f"  - {file.name}")
    else:
        print("✗ No dist directory found")
        sys.exit(1)

def check_packages():
    """Check package quality."""
    print("Checking package quality...")
    run_command("twine check dist/*")

def publish_to_pypi(test=False):
    """Publish packages to PyPI or TestPyPI."""
    print(f"Publishing to {'TestPyPI' if test else 'PyPI'}...")
    
    if test:
        run_command("twine upload --repository testpypi dist/*")
    else:
        run_command("twine upload dist/*")

def main():
    """Main function."""
    print("BiXFlow Release Script")
    print("=" * 30)
    
    # Check prerequisites
    check_prerequisites()
    
    # Clean previous builds
    clean_previous_builds()
    
    # Build packages
    build_packages()
    
    # Check package quality
    check_packages()
    
    # Ask user what to do next
    print("\nWhat would you like to do next?")
    print("1. Publish to TestPyPI (for testing)")
    print("2. Publish to PyPI (production)")
    print("3. Exit (packages are in dist/ directory)")
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == "1":
        publish_to_pypi(test=True)
        print("✓ Published to TestPyPI")
    elif choice == "2":
        publish_to_pypi(test=False)
        print("✓ Published to PyPI")
    elif choice == "3":
        print("Packages are ready in dist/ directory")
        print("You can publish them later using:")
        print("  twine upload dist/*")
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)
    
    print("\nRelease process completed successfully!")

if __name__ == "__main__":
    main()
