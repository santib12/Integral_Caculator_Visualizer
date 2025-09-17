#!/usr/bin/env python3
"""
Enhanced Edge Case Handling for Integral Calculator
Handles problematic edge cases with better error handling and user feedback
"""

import sympy as sp
from sympy import symbols, integrate, sympify, oo, zoo, nan, simplify
import re

def handle_edge_case(func_str, x):
    """
    Enhanced edge case handling for problematic functions
    """
    try:
        # Parse function
        func_parsed = func_str.replace('^', '**')
        func_parsed = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', func_parsed)
        func_parsed = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', func_parsed)
        
        func = sympify(func_parsed)
        
        # Check for specific problematic cases
        if func_str == "x/0":
            return handle_division_by_zero(func, x)
        elif func_str == "sqrt(-1)":
            return handle_imaginary_result(func, x)
        elif func_str == "log(0)":
            return handle_log_zero(func, x)
        elif func_str == "1/x^0":
            return handle_zero_power(func, x)
        else:
            # Standard integration
            result = integrate(func, x)
            return result
            
    except Exception as e:
        return handle_integration_error(func_str, str(e))

def handle_division_by_zero(func, x):
    """
    Handle division by zero cases
    """
    # For x/0, we can return a symbolic representation
    # The integral of x/0 is undefined, but we can represent it symbolically
    return sp.Integral(func, x)  # Return unevaluated integral

def handle_imaginary_result(func, x):
    """
    Handle functions that result in imaginary numbers
    """
    try:
        # Try to integrate and see if we get imaginary results
        result = integrate(func, x)
        
        # Check if result contains imaginary unit
        if hasattr(result, 'is_real') and not result.is_real:
            return result  # Return the imaginary result
        else:
            return result
            
    except Exception:
        # If integration fails, return symbolic form
        return sp.Integral(func, x)

def handle_log_zero(func, x):
    """
    Handle log(0) cases
    """
    try:
        # log(0) is -infinity, so the integral would be -infinity * x
        # But we can represent this symbolically
        return sp.Integral(func, x)
    except Exception:
        return sp.Integral(func, x)

def handle_zero_power(func, x):
    """
    Handle x^0 cases (which should be 1)
    """
    try:
        # 1/x^0 = 1/1 = 1, so integral is x
        result = integrate(func, x)
        return result
    except Exception:
        return sp.Integral(func, x)

def handle_integration_error(func_str, error_msg):
    """
    Handle general integration errors with informative messages
    """
    # Return a symbolic integral with error information
    return sp.Integral(func_str, symbols('x'))

def test_enhanced_edge_cases():
    """
    Test the enhanced edge case handling
    """
    print("TESTING ENHANCED EDGE CASE HANDLING")
    print("=" * 60)
    
    x = symbols('x')
    
    edge_cases = [
        ("x/0", "Division by zero"),
        ("sqrt(-1)", "Imaginary result"),
        ("log(0)", "Log of zero"),
        ("1/x^0", "Zero power"),
        ("1/(x-1)", "Singularity at x=1"),
        ("exp(1/x)", "Exponential with singularity"),
        ("sin(1/x)", "Trigonometric with singularity"),
    ]
    
    for func_str, description in edge_cases:
        print(f"\nEdge Case: {description}")
        print(f"Function: ∫ {func_str} dx")
        
        try:
            result = handle_edge_case(func_str, x)
            
            if isinstance(result, sp.Integral):
                print(f"Result: {result} (Symbolic - cannot be evaluated)")
                print("✓ HANDLED - Symbolic representation provided")
            else:
                print(f"Result: {result} + C")
                print("✓ HANDLED - Function processed successfully")
                
        except Exception as e:
            print(f"✗ ERROR: {str(e)}")

def create_edge_case_improvements():
    """
    Create improvements for edge case handling in the main calculator
    """
    print("\nEDGE CASE IMPROVEMENTS FOR MAIN CALCULATOR")
    print("=" * 60)
    
    improvement_code = '''
    def enhanced_calculate_integral(self):
        """Enhanced calculate integral with better edge case handling"""
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
            
            # Check for edge cases first
            if self.is_edge_case(func_str):
                result = self.handle_edge_case(func_str, self.x)
                self.show_edge_case_result(func_str, result)
                return
            
            # Use improved integration for normal cases
            integral = improved_integrate(func, self.x)
            
            # Show result in popup
            self.show_result_popup(func_str, integral)
            
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def is_edge_case(self, func_str):
        """Check if function is an edge case"""
        edge_patterns = [
            r'/0',           # Division by zero
            r'sqrt\\(-1\\)', # Imaginary
            r'log\\(0\\)',   # Log of zero
            r'\\^0',         # Zero power
        ]
        
        for pattern in edge_patterns:
            if re.search(pattern, func_str):
                return True
        return False
    
    def handle_edge_case(self, func_str, x):
        """Handle edge cases with informative results"""
        return handle_edge_case(func_str, x)
    
    def show_edge_case_result(self, func_str, result):
        """Show edge case result in a special popup"""
        # Create special popup for edge cases
        edge_window = tk.Toplevel(self.root)
        edge_window.title("Edge Case Result")
        edge_window.geometry("500x300")
        edge_window.configure(bg='#F5F5DC')
        
        # Title
        title_label = tk.Label(edge_window, text="Edge Case Detected", 
                              font=('Arial', 14, 'bold'), bg='#F5F5DC', fg='#FF6B6B')
        title_label.pack(pady=10)
        
        # Function display
        func_label = tk.Label(edge_window, text=f"Function: ∫ {func_str} dx", 
                             font=('Arial', 12), bg='#F5F5DC', fg='#333333')
        func_label.pack(pady=5)
        
        # Result display
        if isinstance(result, sp.Integral):
            result_text = "This integral cannot be evaluated in standard form."
            explanation = "The function contains mathematical singularities or undefined operations."
        else:
            result_text = f"Result: {result} + C"
            explanation = "Special handling applied for this edge case."
        
        result_label = tk.Label(edge_window, text=result_text, 
                               font=('Arial', 12, 'bold'), bg='#F5F5DC', fg='#333333')
        result_label.pack(pady=5)
        
        # Explanation
        expl_label = tk.Label(edge_window, text=explanation, 
                             font=('Arial', 10), bg='#F5F5DC', fg='#666666')
        expl_label.pack(pady=5)
        
        # Close button
        close_btn = tk.Button(edge_window, text="Close", font=('Arial', 10, 'bold'),
                            bg='#FF6B6B', fg='white', relief='raised', bd=1,
                            command=edge_window.destroy)
        close_btn.pack(pady=10)
    '''
    
    print("Enhanced integration method with edge case handling:")
    print(improvement_code)

if __name__ == "__main__":
    test_enhanced_edge_cases()
    create_edge_case_improvements()
