#!/usr/bin/env python3
"""
Interactive test for complex integral functions
Allows you to test specific functions manually
"""

import sympy as sp
from sympy import symbols, integrate, latex, sympify, simplify
import re

def test_function():
    """Interactive function testing"""
    print("INTERACTIVE INTEGRAL TESTER")
    print("Enter functions to test (or 'quit' to exit)")
    print("Examples: x^2, sin(x), exp(x), x*sin(x), 1/(x^2+1)")
    
    x = symbols('x')
    
    while True:
        print("\n" + "="*50)
        func_input = input("Enter function to integrate: ").strip()
        
        if func_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
            
        if not func_input:
            print("Please enter a function")
            continue
            
        try:
            # Parse function (same logic as main calculator)
            func_str = func_input.replace('^', '**')
            func_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', func_str)
            func_str = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', func_str)
            
            func = sympify(func_str)
            result = integrate(func, x)
            
            print(f"\nFunction: ∫ {func_input} dx")
            print(f"Result: {result} + C")
            print(f"LaTeX: {latex(result)}")
            
            # Verify by differentiation
            derivative = result.diff(x)
            print(f"Verification (d/dx): {derivative}")
            
            # Check if derivative equals original function
            if simplify(derivative - func) == 0:
                print("✓ VERIFIED - Derivative matches original function")
            else:
                print("⚠ WARNING - Derivative doesn't match original")
                
        except Exception as e:
            print(f"✗ ERROR: {str(e)}")
            print("Try a different function or check syntax")

def quick_test_examples():
    """Quick test of some example functions"""
    print("QUICK TEST EXAMPLES")
    print("="*50)
    
    examples = [
        ("x^2", "Basic polynomial"),
        ("sin(x)", "Trigonometric"),
        ("exp(x)", "Exponential"),
        ("x*sin(x)", "Integration by parts"),
        ("1/(x^2+1)", "Rational function"),
        ("x*exp(x)", "x times exponential"),
        ("sin(x)^2", "Trigonometric identity"),
        ("log(x)", "Logarithmic"),
        ("sqrt(x)", "Power function"),
        ("x*sin(x^2)", "Composite function"),
    ]
    
    x = symbols('x')
    
    for func_str, description in examples:
        try:
            func_parsed = func_str.replace('^', '**')
            func_parsed = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', func_parsed)
            func_parsed = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', func_parsed)
            
            func = sympify(func_parsed)
            result = integrate(func, x)
            
            print(f"\n{description}: ∫ {func_str} dx")
            print(f"Result: {result} + C")
            
        except Exception as e:
            print(f"\n{description}: ∫ {func_str} dx")
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("Choose test mode:")
    print("1. Interactive testing")
    print("2. Quick examples")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        test_function()
    elif choice == "2":
        quick_test_examples()
    else:
        print("Invalid choice. Running quick examples...")
        quick_test_examples()
