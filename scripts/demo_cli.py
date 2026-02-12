#!/usr/bin/env python3
"""Demo script for BiXFlow CLI."""

import subprocess
import sys
import os


def run_command(command):
    """Run a command and print its output."""
    print(f"Running: {' '.join(command)}")
    print("-" * 50)
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, cwd=os.getcwd())
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        print(f"Return code: {result.returncode}")
    except Exception as e:
        print(f"Error running command: {e}")
    
    print("-" * 50)
    print()


def main():
    """Run CLI demos."""
    print("BiXFlow CLI Demo")
    print("=" * 50)
    
    # Show help
    run_command([sys.executable, "-m", "BiXFlow.cli", "--help"])
    
    # List workflows
    run_command([sys.executable, "-m", "BiXFlow.cli", "list-workflows"])
    
    # Show run-named help
    run_command([sys.executable, "-m", "BiXFlow.cli", "run-named", "--help"])
    
    # Show run help
    run_command([sys.executable, "-m", "BiXFlow.cli", "run", "--help"])


if __name__ == "__main__":
    main()
