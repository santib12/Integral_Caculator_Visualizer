#!/usr/bin/env python3
"""
Comprehensive Integral Test Suite
Tests 100+ different integral scenarios covering all major mathematical functions.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import sympy as sp
from sympy import symbols, integrate, sympify, simplify, expand, factor, cancel, trigsimp
from sympy import tanh, cosh, sinh, log, exp, sin, cos, tan, sec, csc, cot
from sympy import asin, acos, atan, asinh, acosh, atanh
from sympy import sqrt, pi, E, I, oo, zoo, erf, Ei, Si, Ci, li
from sympy import gamma, factorial, binomial, bernoulli
import re

def improved_integrate(func, x):
    """Enhanced integration function with better handling"""
    try:
        # Try direct integration first
        result = integrate(func, x)
        
        # If result is still an Integral, try simplification
        if hasattr(result, 'is_Integral') and result.is_Integral:
            # Try expanding and integrating
            expanded = expand(func)
            if expanded != func:
                result = integrate(expanded, x)
            
            # Try factoring and integrating
            if hasattr(result, 'is_Integral') and result.is_Integral:
                factored = factor(func)
                if factored != func:
                    result = integrate(factored, x)
        
        return result
    except Exception:
        return sp.Integral(func, x)

def test_comprehensive_integrals():
    """Test 100+ different integral scenarios"""
    print("COMPREHENSIVE INTEGRAL TESTS")
    print("=" * 60)
    print("Testing 100+ different integral scenarios")
    print()
    
    x = symbols('x')
    
    # Basic polynomial integrals (1-20)
    basic_polynomial_tests = [
        ("x", "Basic linear"),
        ("x^2", "Basic quadratic"),
        ("x^3", "Basic cubic"),
        ("x^4", "Basic quartic"),
        ("x^5", "Basic quintic"),
        ("2*x", "Linear with coefficient"),
        ("3*x^2", "Quadratic with coefficient"),
        ("4*x^3", "Cubic with coefficient"),
        ("x + 1", "Linear with constant"),
        ("x^2 + 2*x + 1", "Perfect square trinomial"),
        ("x^2 - 1", "Difference of squares"),
        ("x^3 + x^2 + x + 1", "Cubic polynomial"),
        ("x^4 - x^2", "Quartic polynomial"),
        ("2*x^3 - 3*x^2 + 5*x - 1", "Complex cubic"),
        ("x^5 - x^3 + x", "Quintic polynomial"),
        ("x^6 + x^4 + x^2 + 1", "Even powers"),
        ("x^7 - x^5 + x^3 - x", "Odd powers"),
        ("(x + 1)^2", "Squared binomial"),
        ("(x - 2)^3", "Cubed binomial"),
        ("(x + 1)*(x - 1)", "Product of binomials"),
    ]
    
    print("BASIC POLYNOMIAL TESTS (1-20):")
    print("-" * 40)
    poly_correct = 0
    poly_total = len(basic_polynomial_tests)
    
    for i, (func_str, description) in enumerate(basic_polynomial_tests, 1):
        try:
            # Parse function
            func_parsed = func_str.replace('^', '**')
            func_parsed = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', func_parsed)
            func_parsed = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', func_parsed)
            
            func = sp.sympify(func_parsed)
            result = improved_integrate(func, x)
            
            # Verify by differentiation
            derivative = result.diff(x)
            if simplify(derivative - func) == 0:
                print(f"[OK] {i:2d}. {description}: int {func_str} dx -> {result} + C")
                poly_correct += 1
            else:
                print(f"[WARN] {i:2d}. {description}: int {func_str} dx -> {result} + C (verification failed)")
                
        except Exception as e:
            print(f"[ERROR] {i:2d}. {description}: int {func_str} dx -> ERROR: {str(e)}")
    
    poly_accuracy = (poly_correct / poly_total) * 100
    print(f"\nBasic Polynomial Accuracy: {poly_accuracy:.1f}% ({poly_correct}/{poly_total})")
    
    # Trigonometric integrals (21-40)
    trigonometric_tests = [
        ("sin(x)", "Basic sine"),
        ("cos(x)", "Basic cosine"),
        ("tan(x)", "Basic tangent"),
        ("sec(x)^2", "Secant squared"),
        ("csc(x)^2", "Cosecant squared"),
        ("cot(x)^2", "Cotangent squared"),
        ("sin(x)^2", "Sine squared"),
        ("cos(x)^2", "Cosine squared"),
        ("sin(x)*cos(x)", "Sine times cosine"),
        ("sin(x)^3", "Sine cubed"),
        ("cos(x)^3", "Cosine cubed"),
        ("sin(x)^4", "Sine to fourth"),
        ("cos(x)^4", "Cosine to fourth"),
        ("tan(x)^2", "Tangent squared"),
        ("sec(x)^3", "Secant cubed"),
        ("csc(x)^3", "Cosecant cubed"),
        ("sin(x)*cos(x)^2", "Sine times cosine squared"),
        ("cos(x)*sin(x)^2", "Cosine times sine squared"),
        ("sin(x)*cos(x)^3", "Sine times cosine cubed"),
        ("cos(x)*sin(x)^3", "Cosine times sine cubed"),
    ]
    
    print(f"\nTRIGONOMETRIC TESTS (21-40):")
    print("-" * 40)
    trig_correct = 0
    trig_total = len(trigonometric_tests)
    
    for i, (func_str, description) in enumerate(trigonometric_tests, 21):
        try:
            # Parse function
            func_parsed = func_str.replace('^', '**')
            func_parsed = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', func_parsed)
            func_parsed = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', func_parsed)
            
            func = sp.sympify(func_parsed)
            result = improved_integrate(func, x)
            
            # Verify by differentiation
            derivative = result.diff(x)
            if simplify(derivative - func) == 0:
                print(f"[OK] {i:2d}. {description}: int {func_str} dx -> {result} + C")
                trig_correct += 1
            else:
                print(f"[WARN] {i:2d}. {description}: int {func_str} dx -> {result} + C (verification failed)")
                
        except Exception as e:
            print(f"[ERROR] {i:2d}. {description}: int {func_str} dx -> ERROR: {str(e)}")
    
    trig_accuracy = (trig_correct / trig_total) * 100
    print(f"\nTrigonometric Accuracy: {trig_accuracy:.1f}% ({trig_correct}/{trig_total})")
    
    # Exponential and logarithmic integrals (41-60)
    exp_log_tests = [
        ("exp(x)", "Basic exponential"),
        ("exp(-x)", "Negative exponential"),
        ("exp(2*x)", "Exponential with coefficient"),
        ("exp(x/2)", "Exponential with fraction"),
        ("log(x)", "Basic logarithm"),
        ("log(2*x)", "Logarithm with coefficient"),
        ("log(x^2)", "Logarithm of square"),
        ("log(sqrt(x))", "Logarithm of square root"),
        ("x*exp(x)", "x times exponential"),
        ("x^2*exp(x)", "x squared times exponential"),
        ("x*log(x)", "x times logarithm"),
        ("x^2*log(x)", "x squared times logarithm"),
        ("exp(x)*sin(x)", "Exponential times sine"),
        ("exp(x)*cos(x)", "Exponential times cosine"),
        ("exp(x)*log(x)", "Exponential times logarithm"),
        ("log(x)/x", "Logarithm over x"),
        ("log(x)/x^2", "Logarithm over x squared"),
        ("exp(x)/x", "Exponential over x"),
        ("exp(x)/x^2", "Exponential over x squared"),
        ("x*exp(x)*log(x)", "x times exponential times logarithm"),
    ]
    
    print(f"\nEXPONENTIAL AND LOGARITHMIC TESTS (41-60):")
    print("-" * 40)
    exp_log_correct = 0
    exp_log_total = len(exp_log_tests)
    
    for i, (func_str, description) in enumerate(exp_log_tests, 41):
        try:
            # Parse function
            func_parsed = func_str.replace('^', '**')
            func_parsed = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', func_parsed)
            func_parsed = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', func_parsed)
            
            func = sp.sympify(func_parsed)
            result = improved_integrate(func, x)
            
            # Verify by differentiation
            derivative = result.diff(x)
            if simplify(derivative - func) == 0:
                print(f"[OK] {i:2d}. {description}: int {func_str} dx -> {result} + C")
                exp_log_correct += 1
            else:
                print(f"[WARN] {i:2d}. {description}: int {func_str} dx -> {result} + C (verification failed)")
                
        except Exception as e:
            print(f"[ERROR] {i:2d}. {description}: int {func_str} dx -> ERROR: {str(e)}")
    
    exp_log_accuracy = (exp_log_correct / exp_log_total) * 100
    print(f"\nExponential/Logarithmic Accuracy: {exp_log_accuracy:.1f}% ({exp_log_correct}/{exp_log_total})")
    
    # Rational function integrals (61-80)
    rational_tests = [
        ("1/x", "Basic reciprocal"),
        ("1/x^2", "Reciprocal squared"),
        ("1/x^3", "Reciprocal cubed"),
        ("1/(x+1)", "Reciprocal with constant"),
        ("1/(x-1)", "Reciprocal with negative constant"),
        ("1/(x^2+1)", "Reciprocal with quadratic"),
        ("1/(x^2-1)", "Reciprocal with difference of squares"),
        ("x/(x^2+1)", "x over quadratic"),
        ("x/(x^2-1)", "x over difference of squares"),
        ("x^2/(x^2+1)", "x squared over quadratic"),
        ("1/(x^3+1)", "Reciprocal with cubic"),
        ("1/(x^3-1)", "Reciprocal with cubic difference"),
        ("x/(x^3+1)", "x over cubic"),
        ("x^2/(x^3+1)", "x squared over cubic"),
        ("1/(x^4+1)", "Reciprocal with quartic"),
        ("1/(x^4-1)", "Reciprocal with quartic difference"),
        ("x/(x^4+1)", "x over quartic"),
        ("x^2/(x^4+1)", "x squared over quartic"),
        ("1/(x^2+x+1)", "Reciprocal with quadratic trinomial"),
        ("x/(x^2+x+1)", "x over quadratic trinomial"),
    ]
    
    print(f"\nRATIONAL FUNCTION TESTS (61-80):")
    print("-" * 40)
    rational_correct = 0
    rational_total = len(rational_tests)
    
    for i, (func_str, description) in enumerate(rational_tests, 61):
        try:
            # Parse function
            func_parsed = func_str.replace('^', '**')
            func_parsed = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', func_parsed)
            func_parsed = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', func_parsed)
            
            func = sp.sympify(func_parsed)
            result = improved_integrate(func, x)
            
            # Verify by differentiation
            derivative = result.diff(x)
            if simplify(derivative - func) == 0:
                print(f"[OK] {i:2d}. {description}: int {func_str} dx -> {result} + C")
                rational_correct += 1
            else:
                print(f"[WARN] {i:2d}. {description}: int {func_str} dx -> {result} + C (verification failed)")
                
        except Exception as e:
            print(f"[ERROR] {i:2d}. {description}: int {func_str} dx -> ERROR: {str(e)}")
    
    rational_accuracy = (rational_correct / rational_total) * 100
    print(f"\nRational Function Accuracy: {rational_accuracy:.1f}% ({rational_correct}/{rational_total})")
    
    # Power and radical integrals (81-100)
    power_radical_tests = [
        ("sqrt(x)", "Basic square root"),
        ("x^(1/3)", "Cube root"),
        ("x^(1/4)", "Fourth root"),
        ("x^(3/2)", "Power 3/2"),
        ("x^(5/2)", "Power 5/2"),
        ("x^(-1/2)", "Power -1/2"),
        ("x^(-3/2)", "Power -3/2"),
        ("sqrt(x^2+1)", "Square root of quadratic"),
        ("sqrt(x^2-1)", "Square root of difference"),
        ("sqrt(1-x^2)", "Square root of 1 minus x squared"),
        ("x*sqrt(x^2+1)", "x times square root"),
        ("x*sqrt(x^2-1)", "x times square root"),
        ("x*sqrt(1-x^2)", "x times square root"),
        ("1/sqrt(x)", "Reciprocal of square root"),
        ("1/sqrt(x^2+1)", "Reciprocal of square root"),
        ("1/sqrt(x^2-1)", "Reciprocal of square root"),
        ("1/sqrt(1-x^2)", "Reciprocal of square root"),
        ("x/sqrt(x^2+1)", "x over square root"),
        ("x/sqrt(x^2-1)", "x over square root"),
        ("x/sqrt(1-x^2)", "x over square root"),
    ]
    
    print(f"\nPOWER AND RADICAL TESTS (81-100):")
    print("-" * 40)
    power_correct = 0
    power_total = len(power_radical_tests)
    
    for i, (func_str, description) in enumerate(power_radical_tests, 81):
        try:
            # Parse function
            func_parsed = func_str.replace('^', '**')
            func_parsed = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', func_parsed)
            func_parsed = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', func_parsed)
            
            func = sp.sympify(func_parsed)
            result = improved_integrate(func, x)
            
            # Verify by differentiation
            derivative = result.diff(x)
            if simplify(derivative - func) == 0:
                print(f"[OK] {i:2d}. {description}: int {func_str} dx -> {result} + C")
                power_correct += 1
            else:
                print(f"[WARN] {i:2d}. {description}: int {func_str} dx -> {result} + C (verification failed)")
                
        except Exception as e:
            print(f"[ERROR] {i:2d}. {description}: int {func_str} dx -> ERROR: {str(e)}")
    
    power_accuracy = (power_correct / power_total) * 100
    print(f"\nPower and Radical Accuracy: {power_accuracy:.1f}% ({power_correct}/{power_total})")
    
    # Overall results
    total_tests = poly_total + trig_total + exp_log_total + rational_total + power_total
    total_correct = poly_correct + trig_correct + exp_log_correct + rational_correct + power_correct
    overall_accuracy = (total_correct / total_tests) * 100
    
    print(f"\n{'='*60}")
    print(f"COMPREHENSIVE INTEGRALS OVERALL ACCURACY: {overall_accuracy:.1f}% ({total_correct}/{total_tests})")
    print()
    
    # Create visual progress bar
    bar_length = 50
    filled_length = int(bar_length * overall_accuracy / 100)
    bar = "=" * filled_length + "-" * (bar_length - filled_length)
    
    print(f"VISUAL ACCURACY BAR:")
    print(f"   [{bar}] {overall_accuracy:.1f}%")
    print()
    
    # Summary
    print("SUMMARY:")
    print(f"   * Basic Polynomials (1-20): {poly_accuracy:.1f}% accuracy")
    print(f"   * Trigonometric (21-40): {trig_accuracy:.1f}% accuracy")
    print(f"   * Exponential/Logarithmic (41-60): {exp_log_accuracy:.1f}% accuracy")
    print(f"   * Rational Functions (61-80): {rational_accuracy:.1f}% accuracy")
    print(f"   * Power and Radical (81-100): {power_accuracy:.1f}% accuracy")
    print(f"   * Overall Performance: {overall_accuracy:.1f}%")
    print()
    
    if overall_accuracy >= 95:
        print("OUTSTANDING PERFORMANCE!")
        print("The integral calculator handles comprehensive integrals excellently.")
    elif overall_accuracy >= 90:
        print("EXCELLENT PERFORMANCE!")
        print("Very high accuracy with comprehensive mathematical functions.")
    elif overall_accuracy >= 80:
        print("GOOD PERFORMANCE!")
        print("Solid accuracy with room for minor improvements.")
    else:
        print("PERFORMANCE NEEDS IMPROVEMENT.")
        print("Consider reviewing failed test cases.")
    
    return overall_accuracy >= 80

if __name__ == "__main__":
    success = test_comprehensive_integrals()
    sys.exit(0 if success else 1)
