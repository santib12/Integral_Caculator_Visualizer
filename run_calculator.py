#!/usr/bin/env python3
"""
Simple launcher script for the Integral Calculator
"""

import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['sympy', 'matplotlib', 'numpy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing required packages:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nTo install missing packages, run:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main launcher function"""
    print("Integral Calculator & Visualizer")
    print("=" * 40)
    
    if not check_dependencies():
        sys.exit(1)
    
    try:
        from integral_calculator import main as run_calculator
        print("Starting calculator...")
        run_calculator()
    except Exception as e:
        print(f"Error starting calculator: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
