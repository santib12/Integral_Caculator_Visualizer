#!/usr/bin/env python3
"""
Setup script for the Integral Calculator & Visualizer
Handles installation and dependency management.
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 or higher is required!")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories if they don't exist"""
    directories = ["src", "tests", "docs", "examples"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")
        else:
            print(f"📁 Directory exists: {directory}")

def verify_installation():
    """Verify that the installation is working"""
    print("\n🔍 Verifying installation...")
    
    try:
        # Test imports
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        
        import sympy
        import matplotlib
        import numpy
        import tkinter
        
        print("✅ All required modules imported successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 INTEGRAL CALCULATOR SETUP")
    print("="*50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Verify installation
    if not verify_installation():
        return False
    
    print("\n🎉 SETUP COMPLETE!")
    print("="*50)
    print("You can now run the integral calculator:")
    print("  python main.py")
    print("\nOr run tests:")
    print("  python run_tests.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
