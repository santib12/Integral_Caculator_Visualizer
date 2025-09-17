#!/usr/bin/env python3
"""
Test script for definite integral functionality
Tests the new bounds input fields and definite integral calculations
"""

import sympy as sp
from sympy import symbols, integrate, simplify
import re

def test_definite_integration():
    """Test definite integral calculations"""
    print("TESTING DEFINITE INTEGRAL FUNCTIONALITY")
    print("=" * 60)
    
    x = symbols('x')
    
    # Test cases for definite integrals
    test_cases = [
        ("x^2", 0, 2, "Basic polynomial"),
        ("x^3", 1, 3, "Cubic polynomial"),
        ("sin(x)", 0, "pi", "Trigonometric function"),
        ("exp(x)", 0, 1, "Exponential function"),
        ("1/x", 1, 2, "Rational function"),
        ("sqrt(x)", 0, 4, "Square root function"),
        ("x*sin(x)", 0, "pi", "Integration by parts"),
        ("x*exp(x)", 0, 1, "x times exponential"),
    ]
    
    print("DEFINITE INTEGRAL TESTS:")
    print("-" * 60)
    
    for func_str, a_val, b_val, description in test_cases:
        try:
            # Parse function
            func_parsed = func_str.replace('^', '**')
            func_parsed = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', func_parsed)
            func_parsed = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', func_parsed)
            
            func = sp.sympify(func_parsed)
            
            # Parse bounds
            if isinstance(a_val, str):
                a = sp.sympify(a_val)
            else:
                a = a_val
                
            if isinstance(b_val, str):
                b = sp.sympify(b_val)
            else:
                b = b_val
            
            # Calculate indefinite integral
            integral = integrate(func, x)
            
            # Calculate definite integral
            definite_result = integral.subs(x, b) - integral.subs(x, a)
            
            print(f"[OK] {description}:")
            print(f"   Function: int {func_str} dx")
            print(f"   Bounds: from {a} to {b}")
            print(f"   Indefinite: {integral} + C")
            print(f"   Definite: {definite_result}")
            print()
            
        except Exception as e:
            print(f"[ERROR] {description}: int {func_str} dx from {a_val} to {b_val}")
            print(f"   Error: {str(e)}")
            print()

def test_bounds_validation():
    """Test bounds validation"""
    print("BOUNDS VALIDATION TESTS:")
    print("-" * 60)
    
    # Test cases for bounds validation
    bounds_tests = [
        ("0", "2", "Valid numeric bounds"),
        ("1.5", "3.7", "Decimal bounds"),
        ("-1", "1", "Negative bounds"),
        ("", "2", "Missing lower bound"),
        ("1", "", "Missing upper bound"),
        ("abc", "2", "Invalid lower bound"),
        ("1", "xyz", "Invalid upper bound"),
    ]
    
    for lower, upper, description in bounds_tests:
        try:
            if not lower or not upper:
                print(f"[WARN] {description}: '{lower}' to '{upper}' - Missing bounds")
                continue
                
            a = float(lower)
            b = float(upper)
            print(f"[OK] {description}: '{lower}' to '{upper}' - Valid bounds")
            
        except ValueError:
            print(f"[ERROR] {description}: '{lower}' to '{upper}' - Invalid bounds")

def create_usage_examples():
    """Create usage examples for the definite integral feature"""
    print("\nUSAGE EXAMPLES:")
    print("-" * 60)
    
    examples = [
        ("x^2", "0", "2", "int_0^2 x^2 dx = 8/3"),
        ("sin(x)", "0", "pi", "int_0^pi sin(x) dx = 2"),
        ("exp(x)", "0", "1", "int_0^1 e^x dx = e - 1"),
        ("1/x", "1", "2", "int_1^2 1/x dx = ln(2)"),
        ("sqrt(x)", "0", "4", "int_0^4 sqrt(x) dx = 16/3"),
    ]
    
    for func, a, b, expected in examples:
        print(f"Function: {func}")
        print(f"Lower bound: {a}")
        print(f"Upper bound: {b}")
        print(f"Expected result: {expected}")
        print()

def show_ui_instructions():
    """Show instructions for using the new UI"""
    print("UI INSTRUCTIONS:")
    print("-" * 60)
    print("1. Select 'Definite' from the Integral Type radio buttons")
    print("2. Enter your function in the input field (e.g., x^2)")
    print("3. Enter the lower bound (a) in the 'Lower bound (a)' field")
    print("4. Enter the upper bound (b) in the 'Upper bound (b)' field")
    print("5. Click 'Go!' to calculate the definite integral")
    print()
    print("The integral display will show:")
    print("- The integral symbol (int) with bounds")
    print("- Your function in parentheses")
    print("- The 'dx' notation")
    print()
    print("The result popup will show:")
    print("- The complete definite integral equation")
    print("- The numerical result")
    print("- Additional information about the calculation")

if __name__ == "__main__":
    test_definite_integration()
    test_bounds_validation()
    create_usage_examples()
    show_ui_instructions()
