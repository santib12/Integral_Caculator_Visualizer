#!/usr/bin/env python3
"""
Complex Integral Test Suite
Tests advanced mathematical functions and complex integration scenarios.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import sympy as sp
from sympy import symbols, integrate, sympify, simplify, expand, factor, cancel, trigsimp
from sympy import tanh, cosh, sinh, log, exp, sin, cos, tan, sec, csc, cot
from sympy import asin, acos, atan, asinh, acosh, atanh
from sympy import sqrt, pi, E, I, oo, zoo
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

def test_complex_integrals():
    """Test complex mathematical integrals"""
    print("COMPLEX INTEGRAL TESTS")
    print("=" * 60)
    print("Testing advanced mathematical functions and complex scenarios")
    print()
    
    x = symbols('x')
    
    # Complex polynomial integrals
    complex_polynomial_tests = [
        ("x^5 + 3*x^4 - 2*x^3 + x^2 - 5*x + 1", "Complex polynomial"),
        ("(x^2 + 1)^3", "Polynomial power"),
        ("x^3/(x^2 + 1)", "Rational polynomial"),
        ("(x^4 - 1)/(x^2 + 1)", "Polynomial division"),
        ("x*sqrt(x^2 + 1)", "Polynomial with radical"),
    ]
    
    print("COMPLEX POLYNOMIAL TESTS:")
    print("-" * 40)
    poly_correct = 0
    poly_total = len(complex_polynomial_tests)
    
    for func_str, description in complex_polynomial_tests:
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
                print(f"[OK] {description}: int {func_str} dx -> {result} + C")
                poly_correct += 1
            else:
                print(f"[WARN] {description}: int {func_str} dx -> {result} + C (verification failed)")
                
        except Exception as e:
            print(f"[ERROR] {description}: int {func_str} dx -> ERROR: {str(e)}")
    
    poly_accuracy = (poly_correct / poly_total) * 100
    print(f"\nComplex Polynomial Accuracy: {poly_accuracy:.1f}% ({poly_correct}/{poly_total})")
    
    # Advanced trigonometric integrals
    advanced_trig_tests = [
        ("sin(x)^3", "Sine cubed"),
        ("cos(x)^3", "Cosine cubed"),
        ("sin(x)^2*cos(x)", "Sine squared times cosine"),
        ("sin(x)*cos(x)^2", "Sine times cosine squared"),
        ("tan(x)^2", "Tangent squared"),
        ("sec(x)^3", "Secant cubed"),
        ("csc(x)^2", "Cosecant squared"),
        ("cot(x)^2", "Cotangent squared"),
        ("sin(x)*cos(x)^3", "Sine times cosine cubed"),
        ("sin(x)^4", "Sine to fourth power"),
    ]
    
    print(f"\nADVANCED TRIGONOMETRIC TESTS:")
    print("-" * 40)
    trig_correct = 0
    trig_total = len(advanced_trig_tests)
    
    for func_str, description in advanced_trig_tests:
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
                print(f"[OK] {description}: int {func_str} dx -> {result} + C")
                trig_correct += 1
            else:
                print(f"[WARN] {description}: int {func_str} dx -> {result} + C (verification failed)")
                
        except Exception as e:
            print(f"[ERROR] {description}: int {func_str} dx -> ERROR: {str(e)}")
    
    trig_accuracy = (trig_correct / trig_total) * 100
    print(f"\nAdvanced Trigonometric Accuracy: {trig_accuracy:.1f}% ({trig_correct}/{trig_total})")
    
    # Hyperbolic function integrals
    hyperbolic_tests = [
        ("sinh(x)^2", "Hyperbolic sine squared"),
        ("cosh(x)^2", "Hyperbolic cosine squared"),
        ("sinh(x)*cosh(x)", "Hyperbolic sine times cosine"),
        ("tanh(x)^2", "Hyperbolic tangent squared"),
        ("sech(x)^2", "Hyperbolic secant squared"),
        ("csch(x)^2", "Hyperbolic cosecant squared"),
        ("coth(x)^2", "Hyperbolic cotangent squared"),
        ("sinh(x)*cosh(x)^2", "Hyperbolic sine times cosine squared"),
        ("cosh(x)*sinh(x)^2", "Hyperbolic cosine times sine squared"),
        ("tanh(x)*sech(x)", "Hyperbolic tangent times secant"),
    ]
    
    print(f"\nHYPERBOLIC FUNCTION TESTS:")
    print("-" * 40)
    hyp_correct = 0
    hyp_total = len(hyperbolic_tests)
    
    for func_str, description in hyperbolic_tests:
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
                print(f"[OK] {description}: int {func_str} dx -> {result} + C")
                hyp_correct += 1
            else:
                print(f"[WARN] {description}: int {func_str} dx -> {result} + C (verification failed)")
                
        except Exception as e:
            print(f"[ERROR] {description}: int {func_str} dx -> ERROR: {str(e)}")
    
    hyp_accuracy = (hyp_correct / hyp_total) * 100
    print(f"\nHyperbolic Function Accuracy: {hyp_accuracy:.1f}% ({hyp_correct}/{hyp_total})")
    
    # Inverse trigonometric integrals
    inverse_trig_tests = [
        ("1/sqrt(1-x^2)", "Inverse sine derivative"),
        ("1/(1+x^2)", "Inverse tangent derivative"),
        ("1/sqrt(x^2-1)", "Inverse hyperbolic cosine derivative"),
        ("1/(1-x^2)", "Inverse hyperbolic tangent derivative"),
        ("x/sqrt(1-x^2)", "x times inverse sine derivative"),
        ("x/(1+x^2)", "x times inverse tangent derivative"),
        ("asin(x)", "Inverse sine"),
        ("atan(x)", "Inverse tangent"),
        ("x*asin(x)", "x times inverse sine"),
        ("x*atan(x)", "x times inverse tangent"),
    ]
    
    print(f"\nINVERSE TRIGONOMETRIC TESTS:")
    print("-" * 40)
    inv_trig_correct = 0
    inv_trig_total = len(inverse_trig_tests)
    
    for func_str, description in inverse_trig_tests:
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
                print(f"[OK] {description}: int {func_str} dx -> {result} + C")
                inv_trig_correct += 1
            else:
                print(f"[WARN] {description}: int {func_str} dx -> {result} + C (verification failed)")
                
        except Exception as e:
            print(f"[ERROR] {description}: int {func_str} dx -> ERROR: {str(e)}")
    
    inv_trig_accuracy = (inv_trig_correct / inv_trig_total) * 100
    print(f"\nInverse Trigonometric Accuracy: {inv_trig_accuracy:.1f}% ({inv_trig_correct}/{inv_trig_total})")
    
    # Complex exponential and logarithmic integrals
    complex_exp_log_tests = [
        ("exp(x^2)", "Exponential of x squared"),
        ("x*exp(x^2)", "x times exponential of x squared"),
        ("exp(x)*sin(x)", "Exponential times sine"),
        ("exp(x)*cos(x)", "Exponential times cosine"),
        ("exp(-x^2)", "Gaussian function"),
        ("x*exp(-x^2)", "x times Gaussian"),
        ("log(x)^2", "Logarithm squared"),
        ("x*log(x)^2", "x times logarithm squared"),
        ("log(x)/x^2", "Logarithm over x squared"),
        ("exp(x)/x", "Exponential over x"),
    ]
    
    print(f"\nCOMPLEX EXPONENTIAL AND LOGARITHMIC TESTS:")
    print("-" * 40)
    exp_log_correct = 0
    exp_log_total = len(complex_exp_log_tests)
    
    for func_str, description in complex_exp_log_tests:
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
                print(f"[OK] {description}: int {func_str} dx -> {result} + C")
                exp_log_correct += 1
            else:
                print(f"[WARN] {description}: int {func_str} dx -> {result} + C (verification failed)")
                
        except Exception as e:
            print(f"[ERROR] {description}: int {func_str} dx -> ERROR: {str(e)}")
    
    exp_log_accuracy = (exp_log_correct / exp_log_total) * 100
    print(f"\nComplex Exponential/Logarithmic Accuracy: {exp_log_accuracy:.1f}% ({exp_log_correct}/{exp_log_total})")
    
    # Integration by parts scenarios
    integration_by_parts_tests = [
        ("x^2*exp(x)", "x squared times exponential"),
        ("x^2*sin(x)", "x squared times sine"),
        ("x^2*cos(x)", "x squared times cosine"),
        ("x^2*log(x)", "x squared times logarithm"),
        ("x^3*exp(x)", "x cubed times exponential"),
        ("x*log(x)^2", "x times logarithm squared"),
        ("x^2*atan(x)", "x squared times inverse tangent"),
        ("x*exp(x)*sin(x)", "x times exponential times sine"),
        ("x*exp(x)*cos(x)", "x times exponential times cosine"),
        ("log(x)*sin(x)", "Logarithm times sine"),
    ]
    
    print(f"\nINTEGRATION BY PARTS TESTS:")
    print("-" * 40)
    ibp_correct = 0
    ibp_total = len(integration_by_parts_tests)
    
    for func_str, description in integration_by_parts_tests:
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
                print(f"[OK] {description}: int {func_str} dx -> {result} + C")
                ibp_correct += 1
            else:
                print(f"[WARN] {description}: int {func_str} dx -> {result} + C (verification failed)")
                
        except Exception as e:
            print(f"[ERROR] {description}: int {func_str} dx -> ERROR: {str(e)}")
    
    ibp_accuracy = (ibp_correct / ibp_total) * 100
    print(f"\nIntegration by Parts Accuracy: {ibp_accuracy:.1f}% ({ibp_correct}/{ibp_total})")
    
    # Overall results
    total_tests = poly_total + trig_total + hyp_total + inv_trig_total + exp_log_total + ibp_total
    total_correct = poly_correct + trig_correct + hyp_correct + inv_trig_correct + exp_log_correct + ibp_correct
    overall_accuracy = (total_correct / total_tests) * 100
    
    print(f"\n{'='*60}")
    print(f"COMPLEX INTEGRALS OVERALL ACCURACY: {overall_accuracy:.1f}% ({total_correct}/{total_tests})")
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
    print(f"   * Complex Polynomials: {poly_accuracy:.1f}% accuracy")
    print(f"   * Advanced Trigonometry: {trig_accuracy:.1f}% accuracy")
    print(f"   * Hyperbolic Functions: {hyp_accuracy:.1f}% accuracy")
    print(f"   * Inverse Trigonometry: {inv_trig_accuracy:.1f}% accuracy")
    print(f"   * Complex Exp/Log: {exp_log_accuracy:.1f}% accuracy")
    print(f"   * Integration by Parts: {ibp_accuracy:.1f}% accuracy")
    print(f"   * Overall Performance: {overall_accuracy:.1f}%")
    print()
    
    if overall_accuracy >= 95:
        print("OUTSTANDING PERFORMANCE!")
        print("The integral calculator handles complex integrals excellently.")
    elif overall_accuracy >= 90:
        print("EXCELLENT PERFORMANCE!")
        print("Very high accuracy with complex mathematical functions.")
    elif overall_accuracy >= 80:
        print("GOOD PERFORMANCE!")
        print("Solid accuracy with room for minor improvements.")
    else:
        print("PERFORMANCE NEEDS IMPROVEMENT.")
        print("Consider reviewing failed test cases.")
    
    return overall_accuracy >= 80

if __name__ == "__main__":
    success = test_complex_integrals()
    sys.exit(0 if success else 1)
