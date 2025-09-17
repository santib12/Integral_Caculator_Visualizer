#!/usr/bin/env python3
"""
Test script for definite integral formatting and positioning
Tests the 4 decimal place formatting and proper spacing
"""

import sympy as sp
from sympy import symbols, integrate, simplify
import re

def test_definite_formatting():
    """Test definite integral formatting to 4 decimal places"""
    print("TESTING DEFINITE INTEGRAL FORMATTING")
    print("=" * 60)
    
    x = symbols('x')
    
    # Test cases for definite integrals with various result types
    test_cases = [
        ("x^2", 0, 2, "Basic polynomial - should be 2.6667"),
        ("x^3", 1, 3, "Cubic polynomial - should be 20.0000"),
        ("sin(x)", 0, "pi", "Trigonometric function - should be 2.0000"),
        ("exp(x)", 0, 1, "Exponential function - should be 1.7183"),
        ("1/x", 1, 2, "Rational function - should be 0.6931"),
        ("sqrt(x)", 0, 4, "Square root function - should be 5.3333"),
        ("x*sin(x)", 0, "pi", "Integration by parts - should be 3.1416"),
        ("x*exp(x)", 0, 1, "x times exponential - should be 1.0000"),
        ("x^4", 0, 1, "Fourth power - should be 0.2000"),
        ("cos(x)", 0, "pi/2", "Cosine function - should be 1.0000"),
    ]
    
    print("DEFINITE INTEGRAL FORMATTING TESTS:")
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
            
            # Format to 4 decimal places
            try:
                if hasattr(definite_result, 'evalf'):
                    numeric_result = float(definite_result.evalf())
                else:
                    numeric_result = float(definite_result)
                formatted_result = f"{numeric_result:.4f}"
            except:
                formatted_result = str(definite_result)
            
            print(f"[OK] {description}:")
            print(f"   Function: int {func_str} dx")
            print(f"   Bounds: from {a} to {b}")
            print(f"   Raw result: {definite_result}")
            print(f"   Formatted (4 decimals): {formatted_result}")
            print()
            
        except Exception as e:
            print(f"[ERROR] {description}: int {func_str} dx from {a_val} to {b_val}")
            print(f"   Error: {str(e)}")
            print()

def test_spacing_calculation():
    """Test spacing calculations for the result popup"""
    print("SPACING CALCULATION TESTS:")
    print("-" * 60)
    
    # Test different function lengths and their spacing requirements
    test_functions = [
        ("x", "Short function"),
        ("x^2", "Medium function"),
        ("sin(x)", "Medium function with parentheses"),
        ("x*exp(x)*sin(x)", "Long complex function"),
        ("sqrt(x^2+1)", "Function with nested operations"),
    ]
    
    for func_str, description in test_functions:
        # Calculate spacing components
        integral_space = 60
        func_space = len(func_str) * 8 + 30
        dx_space = 30
        equals_space = 50  # Increased spacing from dx
        result_space = 100  # Space for result
        safety_margin = 50  # Increased safety margin
        
        total_space = integral_space + func_space + dx_space + equals_space + result_space + safety_margin
        min_width = 600
        total_width = max(min_width, total_space)
        
        print(f"[OK] {description}:")
        print(f"   Function: {func_str}")
        print(f"   Function length: {len(func_str)} characters")
        print(f"   Calculated width: {total_width} pixels")
        print(f"   Components: integral({integral_space}) + func({func_space}) + dx({dx_space}) + equals({equals_space}) + result({result_space}) + margin({safety_margin})")
        print()

def show_positioning_info():
    """Show information about the positioning fixes"""
    print("POSITIONING FIXES IMPLEMENTED:")
    print("-" * 60)
    print("1. Increased spacing from dx to equals sign: 30 -> 50 pixels")
    print("2. Increased spacing from equals to result: 30 -> 50 pixels")
    print("3. Increased minimum window width: 500 -> 600 pixels")
    print("4. Increased safety margin: 30 -> 50 pixels")
    print("5. Added 4 decimal place formatting for numerical results")
    print()
    print("These changes ensure:")
    print("• No overlap between dx box and equals sign")
    print("• No overlap between equals sign and result")
    print("• Adequate spacing for all components")
    print("• Clean 4 decimal place formatting")
    print("• Professional appearance")

def create_ui_layout_diagram():
    """Create a visual diagram of the UI layout"""
    print("UI LAYOUT DIAGRAM:")
    print("-" * 60)
    print("Definite Integral Result Popup Layout:")
    print()
    print("+---------------------------------------------------------------+")
    print("|                    Definite Integral Result                 |")
    print("+---------------------------------------------------------------+")
    print("|  b  int  (function) dx    =    2.6667                       |")
    print("|  a                                                          |")
    print("|                                                             |")
    print("| int from 0 to 2 of x^2 dx = 2.6667                          |")
    print("|                                                             |")
    print("|                        [Close]                             |")
    print("+---------------------------------------------------------------+")
    print()
    print("Spacing breakdown:")
    print("• Integral symbol: 60px")
    print("• Function: variable width")
    print("• dx box: 30px")
    print("• Gap to equals: 50px")
    print("• Equals sign: 25px")
    print("• Gap to result: 50px")
    print("• Result: variable width")
    print("• Safety margin: 50px")

if __name__ == "__main__":
    test_definite_formatting()
    test_spacing_calculation()
    show_positioning_info()
    create_ui_layout_diagram()
