#!/usr/bin/env python3
"""
Main launcher for the Integral Calculator & Visualizer
This is the primary entry point for the application.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the calculator
from src.run_calculator import main

if __name__ == "__main__":
    main()
