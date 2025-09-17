import tkinter as tk
import sympy as sp
from sympy import symbols, integrate, sympify, simplify, expand, factor, cancel, trigsimp
from sympy import tanh, cosh, sinh, log, exp, sin, cos
import re

class IntegralCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculate the Integral of ...")
        self.root.geometry("800x600")
        self.root.configure(bg='#F5F5DC')  # Cream background
        
        # Variables
        self.x = symbols('x')
        self.function_var = tk.StringVar()
        self.integral_type_var = tk.StringVar(value="indefinite")
        self.lower_bound_var = tk.StringVar()
        self.upper_bound_var = tk.StringVar()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container with padding
        main_frame = tk.Frame(self.root, bg='#F5F5DC', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="Calculate the Integral of ...", 
                             font=('Arial', 16, 'bold'), bg='#F5F5DC', fg='#333333')
        title_label.pack(pady=(0, 20))
        
        # Operator buttons frame
        buttons_frame = tk.Frame(main_frame, bg='#F5F5DC')
        buttons_frame.pack(pady=(0, 10))
        
        # Create operator buttons
        operators = ['CLR', '+', '-', '×', '÷', '^', '√', 'f(x)', 'π', '(', ')']
        self.operator_buttons = []
        
        for i, op in enumerate(operators):
            if op == 'CLR':
                btn = tk.Button(buttons_frame, text=op, font=('Arial', 10, 'bold'),
                               bg='white', fg='red', relief='raised', bd=1,
                               command=lambda: self.clear_input())
            else:
                btn = tk.Button(buttons_frame, text=op, font=('Arial', 10),
                               bg='white', fg='#333333', relief='raised', bd=1,
                               command=lambda o=op: self.add_operator(o))
            
            btn.pack(side=tk.LEFT, padx=2)
            self.operator_buttons.append(btn)
        
        # Integral type selection frame
        type_frame = tk.Frame(main_frame, bg='#F5F5DC')
        type_frame.pack(pady=(0, 10))
        
        # Integral type selection
        type_label = tk.Label(type_frame, text="Integral Type:", 
                             font=('Arial', 12, 'bold'), bg='#F5F5DC', fg='#333333')
        type_label.pack(side=tk.LEFT, padx=(0, 10))
        
        indefinite_radio = tk.Radiobutton(type_frame, text="Indefinite", 
                                         variable=self.integral_type_var, value="indefinite",
                                         font=('Arial', 11), bg='#F5F5DC', fg='#333333',
                                         command=self.toggle_bounds)
        indefinite_radio.pack(side=tk.LEFT, padx=(0, 10))
        
        definite_radio = tk.Radiobutton(type_frame, text="Definite", 
                                       variable=self.integral_type_var, value="definite",
                                       font=('Arial', 11), bg='#F5F5DC', fg='#333333',
                                       command=self.toggle_bounds)
        definite_radio.pack(side=tk.LEFT)
        
        # Input field and Go button frame
        input_frame = tk.Frame(main_frame, bg='#F5F5DC')
        input_frame.pack(pady=(0, 10))
        
        # Input field
        self.input_entry = tk.Entry(input_frame, textvariable=self.function_var, 
                                   font=('Arial', 12), width=40, relief='solid', bd=1)
        self.input_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.input_entry.bind('<KeyRelease>', lambda e: self.update_display())
        
        # Go button
        go_btn = tk.Button(input_frame, text="Go!", font=('Arial', 10, 'bold'),
                          bg='#4169E1', fg='white', relief='raised', bd=1,
                          command=self.calculate_integral)
        go_btn.pack(side=tk.LEFT)
        
        # Bounds input frame (initially hidden)
        self.bounds_frame = tk.Frame(main_frame, bg='#F5F5DC')
        
        # Lower bound
        lower_label = tk.Label(self.bounds_frame, text="Lower bound (a):", 
                              font=('Arial', 11), bg='#F5F5DC', fg='#333333')
        lower_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.lower_entry = tk.Entry(self.bounds_frame, textvariable=self.lower_bound_var, 
                                   font=('Arial', 11), width=10, relief='solid', bd=1)
        self.lower_entry.pack(side=tk.LEFT, padx=(0, 15))
        
        # Upper bound
        upper_label = tk.Label(self.bounds_frame, text="Upper bound (b):", 
                              font=('Arial', 11), bg='#F5F5DC', fg='#333333')
        upper_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.upper_entry = tk.Entry(self.bounds_frame, textvariable=self.upper_bound_var, 
                                   font=('Arial', 11), width=10, relief='solid', bd=1)
        self.upper_entry.pack(side=tk.LEFT)
        
        # Subtitle
        subtitle_label = tk.Label(main_frame, text="This will be calculated:", 
                                 font=('Arial', 12, 'bold'), bg='#F5F5DC', fg='#333333')
        subtitle_label.pack(pady=(0, 10))
        
        # Display box with grid background
        self.create_display_box(main_frame)
        
        # Instructions
        instructions_frame = tk.Frame(main_frame, bg='#F5F5DC')
        instructions_frame.pack(pady=(20, 0))
        
        instruction1 = tk.Label(instructions_frame, 
                               text='Use parentheses, if necessary. Also see "Examples".',
                               font=('Arial', 9), bg='#F5F5DC', fg='#666666')
        instruction1.pack(anchor='w')
        
        instruction2 = tk.Label(instructions_frame, 
                               text='Change integration variable and order in "Options".',
                               font=('Arial', 9), bg='#F5F5DC', fg='#666666')
        instruction2.pack(anchor='w')
        
        # Make "Examples" and "Options" underlined (simulated)
        examples_label = tk.Label(instructions_frame, text='"Examples"', 
                                 font=('Arial', 9, 'underline'), bg='#F5F5DC', fg='#666666')
        examples_label.place(x=200, y=0)
        
        options_label = tk.Label(instructions_frame, text='"Options"', 
                                font=('Arial', 9, 'underline'), bg='#F5F5DC', fg='#666666')
        options_label.place(x=200, y=20)
        
    def create_display_box(self, parent):
        """Create the display box with grid background and integral symbol"""
        # Main display frame
        self.display_frame = tk.Frame(parent, bg='#F5F5DC')
        self.display_frame.pack(fill=tk.BOTH, expand=True)
        
        # Display box with light blue border - will be resized dynamically
        self.display_canvas = tk.Canvas(self.display_frame, width=300, height=200, 
                                       bg='white', relief='solid', bd=1,
                                       highlightthickness=2, highlightbackground='#87CEEB')
        self.display_canvas.pack(pady=10)
        
        # TeX label - will be repositioned dynamically
        self.tex_label = tk.Label(self.display_frame, text="TeX", 
                                 font=('Arial', 8), bg='#F5F5DC', fg='#999999')
        self.tex_label.place(x=250, y=220)
        
        # Create grid pattern
        self.create_grid_pattern()
        
        # Create integral symbol and expression
        self.create_integral_display()
        
    def create_grid_pattern(self):
        """Create a subtle grid pattern on the canvas"""
        # Get current canvas dimensions
        canvas_width = self.display_canvas.winfo_reqwidth()
        canvas_height = 200
        
        # Draw grid lines
        for i in range(0, canvas_width, 20):
            self.display_canvas.create_line(i, 0, i, canvas_height, fill='#F0F0F0', width=1)
        for i in range(0, canvas_height, 20):
            self.display_canvas.create_line(0, i, canvas_width, i, fill='#F0F0F0', width=1)
            
    def create_integral_display(self):
        """Create the integral symbol and mathematical expression"""
        # Clear previous drawings
        self.display_canvas.delete("integral")
        
        # Get function text
        func_text = self.function_var.get()
        
        # Convert function to proper mathematical notation
        display_text = self.convert_to_math_notation(func_text)
        
        # Calculate required width based on function length
        # Base width for integral symbol and bounds
        base_width = 150
        # Additional width based on function length (roughly 10 pixels per character)
        function_width = len(display_text) * 10 + 80  # Extra padding
        # Minimum width
        min_width = 300
        # Calculate total width
        total_width = max(min_width, base_width + function_width)
        
        # Resize canvas
        self.display_canvas.config(width=total_width)
        
        # Recreate grid pattern with new width
        self.create_grid_pattern()
        
        # Create proper integral symbol (∫) - use large Unicode symbol
        integral_label = tk.Label(self.display_canvas, text="∫", 
                                 font=('Times New Roman', 80, 'bold'), 
                                 bg='white', fg='#333333')
        self.display_canvas.create_window(100, 100, window=integral_label, tags="integral")
        
        # Add bounds - show actual values if definite integral, placeholders if indefinite
        if self.integral_type_var.get() == "definite":
            # Show actual bound values
            lower_bound = self.lower_bound_var.get() or "a"
            upper_bound = self.upper_bound_var.get() or "b"
            
            # Upper bound
            self.display_canvas.create_rectangle(90, 25, 100, 35, fill='white', 
                                                 outline='#333333', tags="integral")
            self.display_canvas.create_text(95, 30, text=upper_bound, 
                                           font=('Arial', 10, 'bold'), fill='#333333', tags="integral")
            
            # Lower bound
            self.display_canvas.create_rectangle(90, 165, 100, 175, fill='white', 
                                                 outline='#333333', tags="integral")
            self.display_canvas.create_text(95, 170, text=lower_bound, 
                                           font=('Arial', 10, 'bold'), fill='#333333', tags="integral")
        else:
            # Show placeholder squares for indefinite integral
            self.display_canvas.create_rectangle(90, 25, 100, 35, fill='#E0E0E0', 
                                                 outline='#CCCCCC', tags="integral")
            self.display_canvas.create_rectangle(90, 165, 100, 175, fill='#E0E0E0', 
                                                 outline='#CCCCCC', tags="integral")
        
        # Function expression - position based on canvas width
        func_x = min(300, total_width - 150)  # Keep some margin
        # Display function as regular text (no fancy positioning for input display)
        self.display_canvas.create_text(func_x, 100, text=f"({display_text})", 
                                       font=('Arial', 16, 'bold'), fill='#333333', 
                                       tags="integral")
        
        # dx box - position at the end
        dx_frame = tk.Frame(self.display_canvas, bg='#F0F0F0', relief='solid', bd=1)
        dx_label = tk.Label(dx_frame, text="dx", font=('Arial', 12, 'bold'), 
                           bg='#F0F0F0', fg='#333333')
        dx_label.pack(padx=5, pady=2)
        
        # Place dx box at the end of the canvas
        dx_x = total_width - 50
        self.display_canvas.create_window(dx_x, 100, window=dx_frame, tags="integral")
        
        # Reposition TeX label
        self.tex_label.place(x=total_width - 50, y=220)
    
    def improved_integrate(self, func, x):
        """Enhanced integration function that handles special cases better"""
        try:
            # First try standard integration
            result = integrate(func, x)
            
            # Apply simplification and canonical forms for better accuracy
            result = self.simplify_and_canonicalize(result, func, x)
            
            return result
            
        except Exception as e:
            # If standard integration fails, try alternative methods
            return self.handle_special_cases(func, x)
    
    def simplify_and_canonicalize(self, result, original_func, x):
        """Simplify and canonicalize the integration result for better accuracy"""
        # Apply various simplification techniques
        result = simplify(result)
        result = expand(result)
        result = factor(result)
        result = cancel(result)
        
        # For trigonometric results, try trigonometric simplification
        if any(trig in str(result) for trig in ['sin', 'cos', 'tan', 'sinh', 'cosh', 'tanh']):
            result = trigsimp(result)
        
        return result
    
    def handle_special_cases(self, func, x):
        """Handle special cases that might not integrate well with standard methods"""
        func_str = str(func)
        
        # Handle hyperbolic tangent specifically
        if 'tanh' in func_str:
            return self.handle_tanh_integration(func, x)
        
        # Handle complex exponential-trigonometric products
        if 'exp' in func_str and ('sin' in func_str or 'cos' in func_str):
            return self.handle_exponential_trigonometric(func, x)
        
        # Default fallback
        return integrate(func, x)
    
    def handle_tanh_integration(self, func, x):
        """Special handling for tanh(x) integration"""
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
    
    def handle_exponential_trigonometric(self, func, x):
        """Special handling for products of exponential and trigonometric functions"""
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
    
    def is_edge_case(self, func_str):
        """Check if function is an edge case"""
        edge_patterns = [
            r'/0',           # Division by zero
            r'sqrt\(-1\)',   # Imaginary
            r'log\(0\)',     # Log of zero
            r'\^0',          # Zero power
        ]
        
        for pattern in edge_patterns:
            if re.search(pattern, func_str):
                return True
        return False
    
    def handle_edge_case(self, func_str, x):
        """Handle edge cases with informative results"""
        try:
            # Parse function
            func_parsed = func_str.replace('^', '**')
            func_parsed = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', func_parsed)
            func_parsed = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', func_parsed)
            
            func = sympify(func_parsed)
            
            # Check for specific problematic cases
            if func_str == "x/0":
                return sp.Integral(func, x)  # Return unevaluated integral
            elif func_str == "sqrt(-1)":
                result = integrate(func, x)
                return result  # Return imaginary result
            elif func_str == "log(0)":
                return sp.Integral(func, x)  # Return symbolic form
            elif func_str == "1/x^0":
                result = integrate(func, x)
                return result  # Should be x
            else:
                # Standard integration
                result = integrate(func, x)
                return result
                
        except Exception as e:
            return sp.Integral(func_str, x)  # Return symbolic integral
    
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
    
    def toggle_bounds(self):
        """Toggle visibility of bounds input fields based on integral type"""
        if self.integral_type_var.get() == "definite":
            self.bounds_frame.pack(pady=(0, 10))
        else:
            self.bounds_frame.pack_forget()
        self.update_display()
        
    def convert_to_math_notation(self, text):
        """Convert function text to mathematical notation"""
        import re
        
        # Replace superscript patterns (^ followed by digits)
        def replace_superscript(match):
            exponent = match.group(1)
            superscript_map = {
                '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
                '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
            }
            return superscript_map.get(exponent, f'^{exponent}')
        
        # Replace ^digit patterns (more comprehensive)
        text = re.sub(r'\^(\d+)', replace_superscript, text)
        
        # Also handle patterns like "x**2" (SymPy sometimes uses **)
        text = re.sub(r'\*\*(\d+)', lambda m: replace_superscript(m), text)
        
        # Replace multiplication
        text = text.replace('*', '·')
        
        return text
    
    def convert_fractions_to_stacked(self, text):
        """Convert fractions to stacked format (numerator over denominator)"""
        import re
        
        # First, convert superscripts to actual Unicode characters
        text = self.convert_to_math_notation(text)
        
        # Handle +C separately - don't let it connect to fractions
        if ' + C' in text:
            # Split at +C and process the main part
            main_part = text.replace(' + C', '')
            c_part = ' + C'
        else:
            main_part = text
            c_part = ''
        
        # Find patterns like "1/2", "x/3", "x²/4", etc.
        fraction_pattern = r'(\w+(?:[²³⁴⁵⁶⁷⁸⁹⁰¹])?)/(\w+(?:[²³⁴⁵⁶⁷⁸⁹⁰¹])?)'
        
        def replace_fraction(match):
            numerator = match.group(1)
            denominator = match.group(2)
            # Create stacked fraction using Unicode characters
            stacked = f"{numerator}\n—\n{denominator}"
            return stacked
        
        # Replace fractions with stacked format
        result = re.sub(fraction_pattern, replace_fraction, main_part)
        
        # Return result and +C separately so we can handle positioning
        return result, c_part
    
    def create_superscript_text(self, canvas, x, y, base, exponent, font_size=16):
        """Create text with proper superscript positioning"""
        # Create the base text
        canvas.create_text(x, y, text=base, 
                         font=('Arial', font_size, 'bold'), fill='#333333')
        
        # Create the superscript (smaller and positioned above)
        superscript_x = x + len(base) * 8  # Approximate character width
        superscript_y = y - 4  # Position above the base (reduced further for better centering)
        canvas.create_text(superscript_x, superscript_y, text=exponent, 
                         font=('Arial', font_size-4, 'bold'), fill='#333333')
        
    def parse_and_display_exponent(self, canvas, x, y, text, font_size=16):
        """Parse text and display exponents properly positioned"""
        import re
        
        # Find patterns like "x2", "x3", etc. (after superscript conversion)
        pattern = r'(\w)([²³⁴⁵⁶⁷⁸⁹⁰¹])'
        
        last_end = 0
        current_x = x
        
        for match in re.finditer(pattern, text):
            # Display text before the exponent
            before_text = text[last_end:match.start()]
            if before_text:
                canvas.create_text(current_x, y, text=before_text, 
                                 font=('Arial', font_size, 'bold'), fill='#333333')
                current_x += len(before_text) * 8
            
            # Display base and exponent
            base = match.group(1)
            exponent = match.group(2)
            self.create_superscript_text(canvas, current_x, y, base, exponent, font_size)
            current_x += len(base) * 8 + 8  # Base width + superscript width
            
            last_end = match.end()
        
        # Display remaining text
        remaining_text = text[last_end:]
        if remaining_text:
            canvas.create_text(current_x, y, text=remaining_text, 
                             font=('Arial', font_size, 'bold'), fill='#333333')
        
    def add_operator(self, operator):
        """Add operator to input field"""
        current_text = self.function_var.get()
        cursor_pos = self.input_entry.index(tk.INSERT)
        
        if operator == 'f(x)':
            new_text = current_text[:cursor_pos] + 'f(x)' + current_text[cursor_pos:]
        elif operator == 'π':
            new_text = current_text[:cursor_pos] + 'π' + current_text[cursor_pos:]
        else:
            new_text = current_text[:cursor_pos] + operator + current_text[cursor_pos:]
            
        self.function_var.set(new_text)
        self.input_entry.icursor(cursor_pos + len(operator))
        self.update_display()
        
    def clear_input(self):
        """Clear the input field"""
        self.function_var.set("")
        self.update_display()
        
    def update_display(self):
        """Update the integral display"""
        self.create_integral_display()
        
    def calculate_integral(self):
        """Enhanced calculate integral with improved accuracy and edge case handling"""
        try:
            func_str = self.function_var.get().strip()
            if not func_str:
                print("Info: Please enter a function")
                return
            
            # Check if definite integral and bounds are provided
            if self.integral_type_var.get() == "definite":
                lower_bound = self.lower_bound_var.get().strip()
                upper_bound = self.upper_bound_var.get().strip()
                
                if not lower_bound or not upper_bound:
                    print("Info: Please enter both lower and upper bounds for definite integral")
                    return
                
                try:
                    # Parse bounds as numbers
                    a = float(lower_bound)
                    b = float(upper_bound)
                except ValueError:
                    print("Error: Bounds must be valid numbers")
                    return
                
                # Parse function
                func_str = func_str.replace('^', '**')
                func_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', func_str)
                func_str = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', func_str)
                
                func = sympify(func_str)
                
                # Check for edge cases first
                if self.is_edge_case(func_str):
                    result = self.handle_edge_case(func_str, self.x)
                    self.show_edge_case_result(func_str, result)
                    return
                
                # Calculate definite integral
                integral = self.improved_integrate(func, self.x)
                definite_result = integral.subs(self.x, b) - integral.subs(self.x, a)
                
                # Show definite integral result
                self.show_definite_result_popup(func_str, integral, definite_result, a, b)
                return
                
            # Indefinite integral (original logic)
            # Parse function
            func_str = func_str.replace('^', '**')
            func_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', func_str)
            func_str = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', func_str)
            
            func = sympify(func_str)
            
            # Check for edge cases first
            if self.is_edge_case(func_str):
                result = self.handle_edge_case(func_str, self.x)
                self.show_edge_case_result(func_str, result)
                return
            
            # Use improved integration for normal cases
            integral = self.improved_integrate(func, self.x)
            
            # Show result in popup
            self.show_result_popup(func_str, integral)
            
        except Exception as e:
            print(f"Error: Calculation error: {str(e)}")
    
    def show_result_popup(self, func_str, integral):
        """Show result in a popup window with same styling as integral display"""
        # Convert function to proper mathematical notation
        display_func = self.convert_to_math_notation(func_str)
        # Convert integral result to proper mathematical notation first, then handle fractions
        integral_with_superscripts = self.convert_to_math_notation(str(integral))
        display_integral, c_part = self.convert_fractions_to_stacked(integral_with_superscripts)
        
        # Calculate required width for complete equation (snug on left, expandable on right)
        # Account for: integral symbol + function + dx + equals + result + C + minimal margin
        integral_space = 60  # Space for integral symbol (very compact)
        func_space = len(display_func) * 8 + 30  # Function width (very compact)
        dx_space = 30  # dx box space (very compact)
        equals_space = 25  # equals sign (very compact)
        result_space = len(str(integral)) * 12 + 80  # Result width (more space for expansion)
        c_space = 50  # + C space (adequate space)
        safety_margin = 30  # Minimal margin to prevent cutoff
        
        total_space = integral_space + func_space + dx_space + equals_space + result_space + c_space + safety_margin
        min_width = 400  # Very compact minimum for simple equations
        total_width = max(min_width, total_space)
        
        # Create popup window
        result_window = tk.Toplevel(self.root)
        result_window.title("Integral Result")
        result_window.geometry(f"{total_width}x300")  # Increased height for fractions
        result_window.configure(bg='#F5F5DC')  # Same cream background
        result_window.resizable(False, False)
        
        # Center the window
        result_window.transient(self.root)
        result_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(result_window, bg='#F5F5DC')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="Result", 
                              font=('Arial', 14, 'bold'), bg='#F5F5DC', fg='#333333')
        title_label.pack(pady=(0, 10))
        
        # Display canvas with same styling as main integral display
        display_canvas = tk.Canvas(main_frame, width=total_width-20, height=180, 
                                  bg='white', relief='solid', bd=1,
                                  highlightthickness=2, highlightbackground='#87CEEB')
        display_canvas.pack(pady=5)
        
        # Create grid pattern
        for i in range(0, total_width-20, 20):
            display_canvas.create_line(i, 0, i, 180, fill='#F0F0F0', width=1)
        for i in range(0, 180, 20):
            display_canvas.create_line(0, i, total_width-20, i, fill='#F0F0F0', width=1)
        
        # Create result display with same styling as integral
        # Left side: Original integral setup
        # Integral symbol
        integral_label = tk.Label(display_canvas, text="∫", 
                                 font=('Times New Roman', 80, 'bold'), 
                                 bg='white', fg='#333333')
        display_canvas.create_window(100, 75, window=integral_label)
        
        # Function expression - positioned to avoid overlap with integral symbol
        func_x = 140  # Positioned to avoid overlap (100 + 40)
        # Use the same approach as main page - create entire function with parentheses as one text
        # This ensures proper centering like the main page
        display_canvas.create_text(func_x, 75, text=f"({display_func})", 
                                 font=('Arial', 16, 'bold'), fill='#333333')
        
        # dx box - positioned with proper spacing from function
        dx_frame = tk.Frame(display_canvas, bg='#F0F0F0', relief='solid', bd=1)
        dx_label = tk.Label(dx_frame, text="dx", font=('Arial', 12, 'bold'), 
                           bg='#F0F0F0', fg='#333333')
        dx_label.pack(padx=5, pady=2)
        # Calculate dx position based on function width
        func_width = len(f"({display_func})") * 8 + 15  # Reduced padding for tighter spacing
        dx_x = func_x + func_width
        display_canvas.create_window(dx_x, 75, window=dx_frame)
        
        # Equals sign (positioned after dx)
        equals_x = dx_x + 30  # Reduced spacing
        display_canvas.create_text(equals_x, 75, text="=", 
                                 font=('Arial', 20, 'bold'), fill='#333333')
        
        # Right side: Integrated answer + C (moved closer to equals sign)
        result_x = equals_x + 30  # Reduced spacing
        
        # Check if result contains fractions (has newlines)
        if '\n' in display_integral:
            # For fractions, create a multi-line display
            lines = display_integral.split('\n')
            
            # Display each line of the fraction with proper exponent positioning
            for i, line in enumerate(lines):
                y_offset = 75 + (i - 1) * 20  # Center the middle line
                self.parse_and_display_exponent(display_canvas, result_x, y_offset, line, 16)
            
            # Display +C separately, positioned to the right of the fraction
            if c_part:
                # Calculate position for +C (to the right of the fraction)
                fraction_width = max(len(line) for line in lines) * 8 + 20  # Approximate width
                c_x = result_x + fraction_width
                c_y = 75  # Center vertically with the fraction
                display_canvas.create_text(c_x, c_y, text=c_part, 
                                       font=('Arial', 16, 'bold'), fill='#333333')
            else:
                # If no +C was detected, add it manually for indefinite integrals
                fraction_width = max(len(line) for line in lines) * 8 + 20
                c_x = result_x + fraction_width
                c_y = 75
                display_canvas.create_text(c_x, c_y, text=" + C", 
                                       font=('Arial', 16, 'bold'), fill='#333333')
        else:
            # Single line result with proper exponent positioning
            if c_part:
                result_text = display_integral + c_part
            else:
                result_text = display_integral + " + C"
            self.parse_and_display_exponent(display_canvas, result_x, 75, result_text, 16)
        
        # TeX label
        tex_label = tk.Label(main_frame, text="TeX", 
                           font=('Arial', 8), bg='#F5F5DC', fg='#999999')
        tex_label.place(x=total_width-60, y=200)
        
        # Close button
        close_btn = tk.Button(main_frame, text="Close", font=('Arial', 10, 'bold'),
                            bg='#4169E1', fg='white', relief='raised', bd=1,
                            command=result_window.destroy)
        close_btn.pack(pady=(10, 0))
    
    def show_definite_result_popup(self, func_str, integral, definite_result, a, b):
        """Show definite integral result in a popup window"""
        # Convert function to proper mathematical notation
        display_func = self.convert_to_math_notation(func_str)
        # Convert integral result to proper mathematical notation first, then handle fractions
        integral_with_superscripts = self.convert_to_math_notation(str(integral))
        display_integral, c_part = self.convert_fractions_to_stacked(integral_with_superscripts)
        
        # Calculate required width for complete equation with increased spacing
        integral_space = 60
        func_space = len(display_func) * 8 + 30
        dx_space = 30
        equals_space = 50  # Increased spacing from dx
        result_space = len(str(definite_result)) * 12 + 100  # Increased space for result
        safety_margin = 50  # Increased safety margin
        
        total_space = integral_space + func_space + dx_space + equals_space + result_space + safety_margin
        min_width = 600  # Increased minimum width
        total_width = max(min_width, total_space)
        
        # Create popup window
        result_window = tk.Toplevel(self.root)
        result_window.title("Definite Integral Result")
        result_window.geometry(f"{total_width}x350")
        result_window.configure(bg='#F5F5DC')
        result_window.resizable(False, False)
        
        # Center the window
        result_window.transient(self.root)
        result_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(result_window, bg='#F5F5DC')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="Definite Integral Result", 
                              font=('Arial', 14, 'bold'), bg='#F5F5DC', fg='#333333')
        title_label.pack(pady=(0, 10))
        
        # Display canvas with same styling as main integral display
        display_canvas = tk.Canvas(main_frame, width=total_width-20, height=200, 
                                  bg='white', relief='solid', bd=1,
                                  highlightthickness=2, highlightbackground='#87CEEB')
        display_canvas.pack(pady=5)
        
        # Create grid pattern
        for i in range(0, total_width-20, 20):
            display_canvas.create_line(i, 0, i, 200, fill='#F0F0F0', width=1)
        for i in range(0, 200, 20):
            display_canvas.create_line(0, i, total_width-20, i, fill='#F0F0F0', width=1)
        
        # Create definite integral display
        # Integral symbol with bounds
        integral_label = tk.Label(display_canvas, text="∫", 
                                 font=('Times New Roman', 80, 'bold'), 
                                 bg='white', fg='#333333')
        display_canvas.create_window(100, 100, window=integral_label)
        
        # Bounds
        # Upper bound
        display_canvas.create_rectangle(90, 25, 100, 35, fill='white', 
                                       outline='#333333')
        display_canvas.create_text(95, 30, text=str(b), 
                                 font=('Arial', 10, 'bold'), fill='#333333')
        
        # Lower bound
        display_canvas.create_rectangle(90, 165, 100, 175, fill='white', 
                                       outline='#333333')
        display_canvas.create_text(95, 170, text=str(a), 
                                 font=('Arial', 10, 'bold'), fill='#333333')
        
        # Function expression
        func_x = 140
        display_canvas.create_text(func_x, 100, text=f"({display_func})", 
                                 font=('Arial', 16, 'bold'), fill='#333333')
        
        # dx box
        dx_frame = tk.Frame(display_canvas, bg='#F0F0F0', relief='solid', bd=1)
        dx_label = tk.Label(dx_frame, text="dx", font=('Arial', 12, 'bold'), 
                           bg='#F0F0F0', fg='#333333')
        dx_label.pack(padx=5, pady=2)
        func_width = len(f"({display_func})") * 8 + 15
        dx_x = func_x + func_width
        display_canvas.create_window(dx_x, 100, window=dx_frame)
        
        # Equals sign
        equals_x = dx_x + 50  # Increased spacing from dx
        display_canvas.create_text(equals_x, 100, text="=", 
                                 font=('Arial', 20, 'bold'), fill='#333333')
        
        # Result - format to 4 decimal places and position with more spacing
        try:
            # Convert to float and format to 4 decimal places
            if hasattr(definite_result, 'evalf'):
                numeric_result = float(definite_result.evalf())
            else:
                numeric_result = float(definite_result)
            formatted_result = f"{numeric_result:.4f}"
        except:
            # Fallback to string representation if conversion fails
            formatted_result = str(definite_result)
        
        result_x = equals_x + 50  # Increased spacing from equals sign
        display_canvas.create_text(result_x, 100, text=formatted_result, 
                                 font=('Arial', 16, 'bold'), fill='#333333')
        
        # TeX label
        tex_label = tk.Label(main_frame, text="TeX", 
                           font=('Arial', 8), bg='#F5F5DC', fg='#999999')
        tex_label.place(x=total_width-60, y=220)
        
        # Additional info
        info_text = f"∫ from {a} to {b} of {func_str} dx = {formatted_result}"
        info_label = tk.Label(main_frame, text=info_text, 
                             font=('Arial', 11), bg='#F5F5DC', fg='#666666')
        info_label.pack(pady=(10, 0))
        
        # Close button
        close_btn = tk.Button(main_frame, text="Close", font=('Arial', 10, 'bold'),
                            bg='#4169E1', fg='white', relief='raised', bd=1,
                            command=result_window.destroy)
        close_btn.pack(pady=(10, 0))

def main():
    root = tk.Tk()
    app = IntegralCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
