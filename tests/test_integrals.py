#!/usr/bin/env python3
"""
Test suite for complex integral functions
Tests the accuracy and capabilities of the integral calculator
"""

import sympy as sp
from sympy import symbols, integrate, latex, sympify, simplify
import re

def test_integral(func_str, expected_result=None, description=""):
    """Test a single integral and display results"""
    print(f"\n{'='*60}")
    print(f"Test: {description}")
    print(f"Function: int {func_str} dx")
    
    try:
        # Parse function
        func_str_parsed = func_str.replace('^', '**')
        func_str_parsed = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', func_str_parsed)
        func_str_parsed = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', func_str_parsed)
        
        x = symbols('x')
        func = sympify(func_str_parsed)
        result = integrate(func, x)
        
        print(f"Result: {result} + C")
        print(f"LaTeX: {latex(result)}")
        
        if expected_result:
            # Check if results are equivalent
            diff = simplify(result - sympify(expected_result))
            if diff == 0:
                print("[OK] CORRECT - Matches expected result")
            else:
                print(f"[WARN] DIFFERENT - Expected: {expected_result}")
                print(f"Difference: {diff}")
        else:
            print("[OK] CALCULATED - No expected result provided")
            
    except Exception as e:
        print(f"[ERROR] ERROR: {str(e)}")

def run_comprehensive_tests():
    """Run comprehensive test suite"""
    print("COMPREHENSIVE INTEGRAL TEST SUITE")
    print("Testing complex functions with SymPy")
    
    # Test 1: Basic Polynomials
    test_integral("x^2", "x**3/3", "Basic polynomial")
    test_integral("x^3 + 2*x^2 + 5*x + 1", "x**4/4 + 2*x**3/3 + 5*x**2/2 + x", "Complex polynomial")
    
    # Test 2: Trigonometric Functions
    test_integral("sin(x)", "-cos(x)", "Basic sine")
    test_integral("cos(x)", "sin(x)", "Basic cosine")
    test_integral("sin(x)^2", "x/2 - sin(2*x)/4", "Sine squared")
    test_integral("cos(x)^2", "x/2 + sin(2*x)/4", "Cosine squared")
    test_integral("sin(x)*cos(x)", "sin(x)**2/2", "Sine times cosine")
    
    # Test 3: Exponential and Logarithmic
    test_integral("exp(x)", "exp(x)", "Exponential")
    test_integral("x*exp(x)", "exp(x)*(x-1)", "x times exponential")
    test_integral("x^2*exp(x)", "exp(x)*(x**2 - 2*x + 2)", "x squared times exponential")
    test_integral("1/x", "log(x)", "Reciprocal")
    test_integral("log(x)", "x*log(x) - x", "Natural logarithm")
    
    # Test 4: Rational Functions
    test_integral("1/(x^2 + 1)", "atan(x)", "Rational function")
    test_integral("1/(x^2 - 1)", "log(x-1)/2 - log(x+1)/2", "Rational with difference of squares")
    test_integral("x/(x^2 + 1)", "log(x**2 + 1)/2", "x over x squared plus 1")
    
    # Test 5: Power Functions
    test_integral("x^(-1/2)", "2*sqrt(x)", "Square root in denominator")
    test_integral("x^(3/2)", "2*x**(5/2)/5", "Fractional power")
    test_integral("sqrt(x)", "2*x**(3/2)/3", "Square root")
    
    # Test 6: Composite Functions
    test_integral("sin(x^2)*x", "-cos(x**2)/2", "Sine of x squared times x")
    test_integral("exp(x^2)*x", "exp(x**2)/2", "Exponential of x squared times x")
    test_integral("cos(x^3)*x^2", "sin(x**3)/3", "Cosine of x cubed times x squared")
    
    # Test 7: Integration by Parts Cases
    test_integral("x*sin(x)", "sin(x) - x*cos(x)", "x times sine (integration by parts)")
    test_integral("x*cos(x)", "x*sin(x) + cos(x)", "x times cosine (integration by parts)")
    test_integral("x*log(x)", "x**2*log(x)/2 - x**2/4", "x times log (integration by parts)")
    
    # Test 8: Advanced Trigonometric
    test_integral("tan(x)", "-log(cos(x))", "Tangent")
    test_integral("sec(x)^2", "tan(x)", "Secant squared")
    test_integral("csc(x)^2", "-cot(x)", "Cosecant squared")
    
    # Test 9: Hyperbolic Functions
    test_integral("sinh(x)", "cosh(x)", "Hyperbolic sine")
    test_integral("cosh(x)", "sinh(x)", "Hyperbolic cosine")
    test_integral("tanh(x)", "log(cosh(x))", "Hyperbolic tangent")
    
    # Test 10: Very Complex Functions
    test_integral("exp(x)*sin(x)", "exp(x)*sin(x)/2 - exp(x)*cos(x)/2", "Exponential times sine")
    test_integral("exp(x)*cos(x)", "exp(x)*sin(x)/2 + exp(x)*cos(x)/2", "Exponential times cosine")
    test_integral("x*exp(x)*sin(x)", "exp(x)*((x-1)*sin(x) - x*cos(x))/2", "x times exponential times sine")
    
    # Test 11: Special Cases
    test_integral("1/sqrt(1-x^2)", "asin(x)", "Inverse sine derivative")
    test_integral("1/(1+x^2)", "atan(x)", "Inverse tangent derivative")
    test_integral("exp(-x^2)", "sqrt(pi)*erf(x)/2", "Gaussian function (uses error function)")
    
    # Test 12: Challenging Functions
    test_integral("log(x)/x", "log(x)**2/2", "Log over x")
    test_integral("x*sin(x^2)", "-cos(x**2)/2", "x times sine of x squared")
    test_integral("exp(x)/x", "Ei(x)", "Exponential over x (uses exponential integral)")
    
    print(f"\n{'='*60}")
    print("TEST SUITE COMPLETED")
    print("Most functions should show [OK] CORRECT or [OK] CALCULATED")
    print("Functions with special notation (erf, Ei, etc.) are mathematically correct")

def test_edge_cases():
    """Test edge cases and error handling"""
    print(f"\n{'='*60}")
    print("EDGE CASES AND ERROR HANDLING TESTS")
    
    # Test invalid functions
    test_cases = [
        ("", "Empty function"),
        ("x/0", "Division by zero"),
        ("sqrt(-1)", "Imaginary result"),
        ("log(0)", "Log of zero"),
        ("1/x^0", "Zero power"),
    ]
    
    for func, desc in test_cases:
        print(f"\nEdge Case: {desc}")
        print(f"Function: int {func} dx")
        try:
            if func == "":
                print("[ERROR] Empty function")
                continue
                
            func_str_parsed = func.replace('^', '**')
            func_str_parsed = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', func_str_parsed)
            func_str_parsed = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', func_str_parsed)
            
            x = symbols('x')
            func = sympify(func_str_parsed)
            result = integrate(func, x)
            print(f"Result: {result} + C")
            print("[OK] HANDLED - Function processed")
            
        except Exception as e:
            print(f"[ERROR] ERROR: {str(e)}")

if __name__ == "__main__":
    run_comprehensive_tests()
    test_edge_cases()
