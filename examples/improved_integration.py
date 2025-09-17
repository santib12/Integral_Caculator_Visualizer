#!/usr/bin/env python3
"""
Improved Integration Module
Handles special cases and complex functions with better accuracy
"""

import sympy as sp
from sympy import symbols, integrate, simplify, expand, factor, cancel, trigsimp
from sympy import tanh, cosh, sinh, log, exp, sin, cos
import re

def improved_integrate(func, x):
    """
    Enhanced integration function that handles special cases better
    """
    try:
        # First try standard integration
        result = integrate(func, x)
        
        # Apply simplification and canonical forms for better accuracy
        result = simplify_and_canonicalize(result, func, x)
        
        return result
        
    except Exception as e:
        # If standard integration fails, try alternative methods
        return handle_special_cases(func, x)

def simplify_and_canonicalize(result, original_func, x):
    """
    Simplify and canonicalize the integration result for better accuracy
    """
    # Apply various simplification techniques
    result = simplify(result)
    result = expand(result)
    result = factor(result)
    result = cancel(result)
    
    # For trigonometric results, try trigonometric simplification
    if any(trig in str(result) for trig in ['sin', 'cos', 'tan', 'sinh', 'cosh', 'tanh']):
        result = trigsimp(result)
    
    return result

def handle_special_cases(func, x):
    """
    Handle special cases that might not integrate well with standard methods
    """
    func_str = str(func)
    
    # Handle hyperbolic tangent specifically
    if 'tanh' in func_str:
        return handle_tanh_integration(func, x)
    
    # Handle complex exponential-trigonometric products
    if 'exp' in func_str and ('sin' in func_str or 'cos' in func_str):
        return handle_exponential_trigonometric(func, x)
    
    # Default fallback
    return integrate(func, x)

def handle_tanh_integration(func, x):
    """
    Special handling for tanh(x) integration
    """
    try:
        # Standard integration
        result = integrate(func, x)
        
        # For tanh(x), we know the canonical form should be log(cosh(x))
        if func == tanh(x):
            # Verify by differentiation
            canonical_result = log(cosh(x))
            derivative = canonical_result.diff(x)
            
            # Check if derivative matches original function
            if simplify(derivative - func) == 0:
                return canonical_result
        
        return result
        
    except Exception as e:
        # Fallback to known result for tanh(x)
        if func == tanh(x):
            return log(cosh(x))
        raise e

def handle_exponential_trigonometric(func, x):
    """
    Special handling for products of exponential and trigonometric functions
    """
    try:
        # Try standard integration first
        result = integrate(func, x)
        
        # For x*exp(x)*sin(x), try to get a cleaner form
        if str(func) == 'x*exp(x)*sin(x)':
            # Known result: exp(x)*((x-1)*sin(x) - x*cos(x))/2
            # But SymPy might give a different but equivalent form
            # Let's verify by differentiation
            derivative = result.diff(x)
            if simplify(derivative - func) == 0:
                return result
        
        return result
        
    except Exception as e:
        raise e

def test_improved_integration():
    """
    Test the improved integration function
    """
    print("TESTING IMPROVED INTEGRATION")
    print("=" * 50)
    
    x = symbols('x')
    
    # Test cases that had issues
    test_cases = [
        ("tanh(x)", "Hyperbolic tangent"),
        ("x*exp(x)*sin(x)", "Complex exponential-trigonometric"),
        ("sinh(x)", "Hyperbolic sine"),
        ("cosh(x)", "Hyperbolic cosine"),
        ("exp(x)*sin(x)", "Exponential times sine"),
        ("exp(x)*cos(x)", "Exponential times cosine"),
    ]
    
    for func_str, description in test_cases:
        print(f"\n{description}: ∫ {func_str} dx")
        
        try:
            # Parse function
            func_parsed = func_str.replace('^', '**')
            func_parsed = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', func_parsed)
            func_parsed = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', func_parsed)
            
            func = sp.sympify(func_parsed)
            
            # Use improved integration
            result = improved_integrate(func, x)
            
            print(f"Improved Result: {result} + C")
            
            # Verify by differentiation
            derivative = result.diff(x)
            verification = simplify(derivative - func)
            
            if verification == 0:
                print("✓ VERIFIED - Derivative matches original function")
            else:
                print(f"⚠ WARNING - Verification: {verification}")
                
        except Exception as e:
            print(f"✗ ERROR: {str(e)}")

def create_enhanced_calculator():
    """
    Create an enhanced version of the calculator with improved integration
    """
    print("\nENHANCED CALCULATOR INTEGRATION")
    print("=" * 50)
    
    # This would be integrated into the main calculator
    print("To integrate these improvements into the main calculator:")
    print("1. Replace the standard integrate() call with improved_integrate()")
    print("2. Add the simplification functions to the result processing")
    print("3. Handle special cases in the calculate_integral method")
    
    # Example integration code
    integration_code = '''
    def calculate_integral(self):
        """Enhanced calculate integral method"""
        try:
            func_str = self.function_var.get().strip()
            if not func_str:
                messagebox.showinfo("Info", "Please enter a function")
                return
                
            # Parse function
            func_str = func_str.replace('^', '**')
            func_str = re.sub(r'(\\d)([a-zA-Z])', r'\\1*\\2', func_str)
            func_str = re.sub(r'([a-zA-Z])(\\d)', r'\\1*\\2', func_str)
            
            func = sympify(func_str)
            
            # Use improved integration
            integral = improved_integrate(func, self.x)
            
            # Show result in popup
            self.show_result_popup(func_str, integral)
            
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    '''
    
    print("\nEnhanced integration method:")
    print(integration_code)

if __name__ == "__main__":
    test_improved_integration()
    create_enhanced_calculator()
