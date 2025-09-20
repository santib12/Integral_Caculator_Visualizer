import tkinter as tk
import sympy as sp
from sympy import symbols, integrate, sympify, simplify, expand, factor, cancel, trigsimp
from sympy import tanh, cosh, sinh, log, exp, sin, cos
import re
from tkinter import font as tkfont
from sympy import nsimplify, pi, E

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
        # Base width for integral symbol, bounds, dx, and generous spacing
        base_width = 300  # More space for integral symbol + bounds + dx + generous spacing
        # Additional width based on function length (very generous spacing for longer equations)
        function_width = len(display_text) * 15 + 150  # Increased character width and padding
        # Minimum width
        min_width = 500  # Increased minimum to accommodate better spacing
        # Maximum width to prevent excessive expansion but allow for long equations
        max_width = 1600  # Increased maximum for very long equations
        # Calculate total width
        total_width = max(min_width, min(max_width, base_width + function_width))
        
        # Resize canvas
        self.display_canvas.config(width=total_width)
        
        # Recreate grid pattern with new width
        self.create_grid_pattern()
        
        # Create proper integral symbol (∫) - positioned at fixed left position
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
        
        # Function expression - positioned well after integral symbol to avoid overlap
        func_x = 200  # Further increased distance from integral symbol for longer equations
        # Display function as regular text
        self.display_canvas.create_text(func_x, 100, text=f"({display_text})", 
                                       font=('Arial', 16, 'bold'), fill='#333333', 
                                       tags="integral")
        
        # dx box - positioned after function with proper spacing
        dx_frame = tk.Frame(self.display_canvas, bg='#F0F0F0', relief='solid', bd=1)
        dx_label = tk.Label(dx_frame, text="dx", font=('Arial', 12, 'bold'), 
                           bg='#F0F0F0', fg='#333333')
        dx_label.pack(padx=5, pady=2)
        
        # Calculate dx position based on function width
        func_width = len(f"({display_text})") * 10 + 20  # Approximate character width
        dx_x = func_x + func_width + 20  # Add spacing after function
        self.display_canvas.create_window(dx_x, 100, window=dx_frame, tags="integral")
        
        # Reposition TeX label to stay at right edge
        self.tex_label.place(x=total_width - 50, y=220)
    
    def improved_integrate(self, func, x):
        """Enhanced integration function that handles special cases better"""
        try:
            # First try standard integration
            result = integrate(func, x)
            
            # Apply simplification and canonical forms for better accuracy
            result = self.simplify_and_canonicalize(result, func, x)
            
            # Verify antiderivative; try manualintegrate if needed
            if not self.verify_antiderivative(func, result, x):
                try:
                    from sympy.integrals.manualintegrate import manualintegrate
                    alt = manualintegrate(func, x)
                    alt = self.simplify_expr(alt)
                    if self.verify_antiderivative(func, alt, x):
                        return alt
                except Exception:
                    pass
            
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
    
    def convert_fractions_to_horizontal(self, text):
        """Convert stacked fractions back to horizontal format for better space utilization"""
        import re
        
        # Handle stacked fractions (numerator\n—\ndenominator)
        # Replace with horizontal format: (numerator)/(denominator)
        stacked_pattern = r'(\w+(?:[²³⁴⁵⁶⁷⁸⁹⁰¹])?)\n—\n(\w+(?:[²³⁴⁵⁶⁷⁸⁹⁰¹])?)'
        
        def replace_stacked_fraction(match):
            numerator = match.group(1)
            denominator = match.group(2)
            # Create horizontal fraction
            horizontal = f"({numerator})/({denominator})"
            return horizontal
        
        # Replace stacked fractions with horizontal format
        result = re.sub(stacked_pattern, replace_stacked_fraction, text)
        
        return result

    def wrap_text_for_canvas(self, text, max_width_px, font_obj):
        """Wrap a math string to fit within max_width_px using font metrics.
        Breaks preferentially at spaces and common operators.
        Returns a list of lines.
        """
        if not text:
            return [""]

        # Insert spaces around typical math operators to create breakpoints
        # Include common unicode operators used in UI
        operators_pattern = r"([+\-*/^=(),]|·|×|÷)"
        preprocessed = re.sub(operators_pattern, r" \1 ", text)

        tokens = preprocessed.split()
        lines = []
        current_line_tokens = []

        def measured_width(tokens_list):
            # Join with single spaces for display spacing
            return font_obj.measure(" ".join(tokens_list))

        for token in tokens:
            if not current_line_tokens:
                current_line_tokens.append(token)
                continue

            trial = current_line_tokens + [token]
            if measured_width(trial) <= max_width_px:
                current_line_tokens.append(token)
            else:
                # Commit current line and start new
                lines.append(" ".join(current_line_tokens))
                current_line_tokens = [token]

        if current_line_tokens:
            lines.append(" ".join(current_line_tokens))

        # Fallback: ensure at least one line
        if not lines:
            lines = [text]

        return lines

    def simplify_expr(self, expr):
        """Apply a sequence of simplifications to get a cleaner, equivalent form."""
        try:
            simplified = simplify(expr)
            simplified = cancel(simplified)
            simplified = factor(simplified)
            simplified = sp.together(simplified)
            simplified = sp.radsimp(simplified)
            simplified = trigsimp(simplified)
            try:
                simplified = nsimplify(simplified, [pi, E])
            except Exception:
                pass
            return simplified
        except Exception:
            return expr

    def verify_antiderivative(self, func, F, x):
        """Return True if dF/dx simplifies to func."""
        try:
            check = simplify(sp.diff(F, x) - func)
            return check == 0
        except Exception:
            return False

    def parse_bound(self, bound_str):
        """Parse a bound string into a SymPy expression supporting π and ^ syntax."""
        s = (bound_str or "").strip()
        if not s:
            raise ValueError("Empty bound")
        s = s.replace('^', '**')
        s = s.replace('π', 'pi')
        s = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', s)
        s = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', s)
        return sympify(s)
    
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
                
                # Parse bounds as SymPy for exact arithmetic where possible
                try:
                    A = self.parse_bound(lower_bound)
                    B = self.parse_bound(upper_bound)
                except Exception:
                    print("Error: Bounds must be valid numbers or expressions (e.g., 0, 1, pi/2)")
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
                
                # Calculate antiderivative and exact definite integral if possible
                integral = self.improved_integrate(func, self.x)
                integral = self.simplify_expr(integral)

                try:
                    exact_def = integrate(func, (self.x, A, B))
                except Exception:
                    exact_def = sp.Integral(func, (self.x, A, B))

                if isinstance(exact_def, sp.Integral):
                    # Fallback to Fundamental Theorem of Calculus
                    try:
                        exact_def = integral.subs(self.x, B) - integral.subs(self.x, A)
                    except Exception:
                        exact_def = sp.Integral(func, (self.x, A, B))

                exact_def = self.simplify_expr(exact_def)

                # Numeric approximation
                try:
                    numeric_val = float(exact_def.evalf())
                except Exception:
                    try:
                        numeric_val = float((integral.subs(self.x, B) - integral.subs(self.x, A)).evalf())
                    except Exception:
                        numeric_val = None

                # Show definite integral result (display exact, include numeric approx)
                self.show_definite_result_popup(
                    func_str,
                    integral,
                    exact_def,
                    self.convert_to_math_notation(lower_bound),
                    self.convert_to_math_notation(upper_bound),
                    numeric_val,
                )
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
            integral = self.simplify_expr(integral)
            
            # Show result in popup
            self.show_result_popup(func_str, integral)
            
        except Exception as e:
            print(f"Error: Calculation error: {str(e)}")
    
    def show_result_popup(self, func_str, integral):
        """Show result in a popup window with improved layout for longer equations"""
        # Convert function to proper mathematical notation
        display_func = self.convert_to_math_notation(func_str)
        # Convert integral result to proper mathematical notation - keep horizontal format
        integral_with_superscripts = self.convert_to_math_notation(str(integral))
        display_integral = integral_with_superscripts
        c_part = " + C"  # Always add +C for indefinite integrals
        
        # Calculate required width dynamically based on actual equation components
        # More accurate spacing calculation for even distribution
        
        # Calculate actual text widths using font metrics
        font_size = 16
        char_width = font_size * 0.6  # Approximate character width for Arial font
        
        # Component spacing calculations
        integral_symbol_width = 80  # Width of the integral symbol
        integral_bounds_width = 20  # Space for bounds
        integral_total_width = integral_symbol_width + integral_bounds_width
        
        function_text_width = len(display_func) * char_width + 20  # Function text + reduced padding
        dx_box_width = 30  # dx box width (reduced)
        equals_width = 15  # equals sign width (reduced)
        
        # Calculate result width more accurately for longer equations
        # Account for stacked fractions and complex expressions
        result_str = str(integral)
        if '/' in result_str:
            # For fractions, estimate width based on longest part
            parts = result_str.split('/')
            max_part_width = max(len(part) for part in parts) * char_width
            result_text_width = max_part_width + 40  # Extra space for fraction formatting
        else:
            result_text_width = len(result_str) * char_width + 20  # Standard width
        
        c_text_width = len(" + C") * char_width  # + C text width
        
        # Spacing between components (tighter for better content hugging)
        component_spacing = 20  # Reduced from 30 for tighter spacing
        
        # Calculate total required width with safety factor for longer equations
        total_equation_width = (integral_total_width + component_spacing + 
                               function_text_width + component_spacing + 
                               dx_box_width + component_spacing + 
                               equals_width + component_spacing + 
                               result_text_width + component_spacing + 
                               c_text_width)
        
        # Add safety factor for very long equations to prevent stacking
        safety_factor = 1.2  # 20% extra space for complex expressions
        total_equation_width = int(total_equation_width * safety_factor)
        
        # Add tighter margins for better content hugging
        left_margin = 30  # Reduced from 50
        right_margin = 30  # Reduced from 50
        total_width = int(total_equation_width + left_margin + right_margin)
        
        # Set tighter bounds for better content hugging
        min_width = 400  # Reduced from 600 for shorter equations
        max_width = 2500  # Increased to accommodate longer equations with stacked fractions
        total_width = max(min_width, min(max_width, total_width))
        
        # Create popup window
        result_window = tk.Toplevel(self.root)
        result_window.title("Integral Result")
        result_window.geometry(f"{total_width}x350")  # Increased height for better layout
        result_window.configure(bg='#F5F5DC')  # Same cream background
        result_window.resizable(False, False)
        
        # Center the window
        result_window.transient(self.root)
        result_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(result_window, bg='#F5F5DC')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Title
        title_label = tk.Label(main_frame, text="Result", 
                              font=('Arial', 14, 'bold'), bg='#F5F5DC', fg='#333333')
        title_label.pack(pady=(0, 15))
        
        # Display canvas with same styling as main integral display
        display_canvas = tk.Canvas(main_frame, width=total_width-30, height=200, 
                                  bg='white', relief='solid', bd=1,
                                  highlightthickness=2, highlightbackground='#87CEEB')
        display_canvas.pack(pady=10)
        
        # Create grid pattern
        for i in range(0, total_width-30, 20):
            display_canvas.create_line(i, 0, i, 200, fill='#F0F0F0', width=1)
        for i in range(0, 200, 20):
            display_canvas.create_line(0, i, total_width-30, i, fill='#F0F0F0', width=1)
        
        # Create result display with dynamic positioning for even spacing
        # Calculate positions based on actual component widths
        
        # Start position (left margin)
        start_x = left_margin
        
        # Integral symbol position
        integral_x = start_x + integral_symbol_width // 2
        integral_label = tk.Label(display_canvas, text="∫", 
                                 font=('Times New Roman', 80, 'bold'), 
                                 bg='white', fg='#333333')
        display_canvas.create_window(integral_x, 100, window=integral_label)
        
        # Function expression position
        func_x = start_x + integral_total_width + component_spacing + function_text_width // 2
        display_canvas.create_text(func_x, 100, text=f"({display_func})", 
                                 font=('Arial', 16, 'bold'), fill='#333333')
        
        # dx box position
        dx_x = start_x + integral_total_width + component_spacing + function_text_width + component_spacing + dx_box_width // 2
        dx_frame = tk.Frame(display_canvas, bg='#F0F0F0', relief='solid', bd=1)
        dx_label = tk.Label(dx_frame, text="dx", font=('Arial', 12, 'bold'), 
                           bg='#F0F0F0', fg='#333333')
        dx_label.pack(padx=5, pady=2)
        display_canvas.create_window(dx_x, 100, window=dx_frame)
        
        # Equals sign position
        equals_x = start_x + integral_total_width + component_spacing + function_text_width + component_spacing + dx_box_width + component_spacing + equals_width // 2
        display_canvas.create_text(equals_x, 100, text="=", 
                                 font=('Arial', 20, 'bold'), fill='#333333')
        
        # Compute available result area and center x
        result_left_x = (start_x + integral_total_width + component_spacing +
                         function_text_width + component_spacing + dx_box_width +
                         component_spacing + equals_width + component_spacing)
        available_result_width = (total_width - right_margin) - result_left_x
        result_x = int(result_left_x + available_result_width / 2)
        
        # Convert fractions to stacked format for better mathematical display
        stacked_result, c_part_stacked = self.convert_fractions_to_stacked(display_integral + c_part)
        
        # Check if result contains fractions (has newlines)
        if '\n' in stacked_result:
            # For fractions, create a multi-line display with proper positioning
            lines = stacked_result.split('\n')
            
            # Calculate tighter vertical positioning for fractions
            # Reduce spacing between numerator, fraction bar, and denominator
            line_spacing = 15  # Reduced from 20 for tighter spacing
            fraction_height = len(lines) * line_spacing
            start_y = 100 - (fraction_height // 2) + 5  # Reduced offset for better centering
            
            # Display each line of the fraction with tighter spacing
            for i, line in enumerate(lines):
                y_offset = start_y + (i * line_spacing)
                display_canvas.create_text(result_x, y_offset, text=line, 
                                         font=('Arial', 16, 'bold'), fill='#333333')
        else:
            # Non-fraction: wrap to available width using font metrics
            font_obj = tkfont.Font(family='Arial', size=16, weight='bold')
            wrapped_lines = self.wrap_text_for_canvas(stacked_result, int(available_result_width), font_obj)
            line_spacing = int(font_obj.metrics('linespace') * 1.2) or 20
            start_y = int(100 - (len(wrapped_lines) - 1) * line_spacing / 2)
            for i, line in enumerate(wrapped_lines):
                y = start_y + i * line_spacing
                display_canvas.create_text(result_x, y, text=line,
                                           font=('Arial', 16, 'bold'), fill='#333333')
        
        # TeX label
        tex_label = tk.Label(main_frame, text="TeX", 
                           font=('Arial', 8), bg='#F5F5DC', fg='#999999')
        tex_label.place(x=total_width-60, y=230)
        
        # Close button
        close_btn = tk.Button(main_frame, text="Close", font=('Arial', 10, 'bold'),
                            bg='#4169E1', fg='white', relief='raised', bd=1,
                            command=result_window.destroy)
        close_btn.pack(pady=(15, 0))
    
    def show_definite_result_popup(self, func_str, integral, definite_result_exact, a_display, b_display, numeric_result):
        """Show definite integral result in a popup window with improved layout"""
        # Convert function to proper mathematical notation
        display_func = self.convert_to_math_notation(func_str)
        # Convert integral result to proper mathematical notation - keep horizontal format
        integral_with_superscripts = self.convert_to_math_notation(str(integral))
        display_integral = integral_with_superscripts
        
        # Calculate required width dynamically based on actual equation components
        # More accurate spacing calculation for even distribution
        
        # Calculate actual text widths using font metrics
        font_size = 16
        char_width = font_size * 0.6  # Approximate character width for Arial font
        
        # Component spacing calculations
        integral_symbol_width = 80  # Width of the integral symbol
        integral_bounds_width = 20  # Space for bounds
        integral_total_width = integral_symbol_width + integral_bounds_width
        
        function_text_width = len(display_func) * char_width + 20  # Function text + reduced padding
        dx_box_width = 30  # dx box width (reduced)
        equals_width = 15  # equals sign width (reduced)
        
        # Calculate result width based on exact symbolic result
        result_str = str(definite_result_exact)
        if '/' in result_str:
            # For fractions, estimate width based on longest part
            parts = result_str.split('/')
            max_part_width = max(len(part) for part in parts) * char_width
            result_text_width = max_part_width + 40  # Extra space for fraction formatting
        else:
            result_text_width = len(result_str) * char_width + 20  # Standard width
        
        # Spacing between components (tighter for better content hugging)
        component_spacing = 20  # Reduced from 30 for tighter spacing
        
        # Calculate total required width with safety factor for longer equations
        total_equation_width = (integral_total_width + component_spacing + 
                               function_text_width + component_spacing + 
                               dx_box_width + component_spacing + 
                               equals_width + component_spacing + 
                               result_text_width)
        
        # Add safety factor for very long equations to prevent stacking
        safety_factor = 1.2  # 20% extra space for complex expressions
        total_equation_width = int(total_equation_width * safety_factor)
        
        # Add tighter margins for better content hugging
        left_margin = 30  # Reduced from 50
        right_margin = 30  # Reduced from 50
        total_width = int(total_equation_width + left_margin + right_margin)
        
        # Set tighter bounds for better content hugging
        min_width = 400  # Reduced from 600 for shorter equations
        max_width = 2500  # Increased to accommodate longer equations with stacked fractions
        total_width = max(min_width, min(max_width, total_width))
        
        # Create popup window
        result_window = tk.Toplevel(self.root)
        result_window.title("Definite Integral Result")
        result_window.geometry(f"{total_width}x400")  # Increased height for better layout
        result_window.configure(bg='#F5F5DC')
        result_window.resizable(False, False)
        
        # Center the window
        result_window.transient(self.root)
        result_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(result_window, bg='#F5F5DC')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Title
        title_label = tk.Label(main_frame, text="Definite Integral Result", 
                              font=('Arial', 14, 'bold'), bg='#F5F5DC', fg='#333333')
        title_label.pack(pady=(0, 15))
        
        # Display canvas with same styling as main integral display
        display_canvas = tk.Canvas(main_frame, width=total_width-30, height=220, 
                                  bg='white', relief='solid', bd=1,
                                  highlightthickness=2, highlightbackground='#87CEEB')
        display_canvas.pack(pady=10)
        
        # Create grid pattern
        for i in range(0, total_width-30, 20):
            display_canvas.create_line(i, 0, i, 220, fill='#F0F0F0', width=1)
        for i in range(0, 220, 20):
            display_canvas.create_line(0, i, total_width-30, i, fill='#F0F0F0', width=1)
        
        # Create definite integral display with dynamic positioning for even spacing
        # Calculate positions based on actual component widths
        
        # Start position (left margin)
        start_x = left_margin
        
        # Integral symbol position
        integral_x = start_x + integral_symbol_width // 2
        integral_label = tk.Label(display_canvas, text="∫", 
                                 font=('Times New Roman', 80, 'bold'), 
                                 bg='white', fg='#333333')
        display_canvas.create_window(integral_x, 110, window=integral_label)
        
        # Bounds positioned relative to integral symbol
        # Upper bound
        display_canvas.create_rectangle(integral_x - 10, 35, integral_x, 45, fill='white', 
                                       outline='#333333')
        display_canvas.create_text(integral_x - 5, 40, text=str(b_display), 
                                 font=('Arial', 10, 'bold'), fill='#333333')
        
        # Lower bound
        display_canvas.create_rectangle(integral_x - 10, 175, integral_x, 185, fill='white', 
                                       outline='#333333')
        display_canvas.create_text(integral_x - 5, 180, text=str(a_display), 
                                 font=('Arial', 10, 'bold'), fill='#333333')
        
        # Function expression position
        func_x = start_x + integral_total_width + component_spacing + function_text_width // 2
        display_canvas.create_text(func_x, 110, text=f"({display_func})", 
                                 font=('Arial', 16, 'bold'), fill='#333333')
        
        # dx box position
        dx_x = start_x + integral_total_width + component_spacing + function_text_width + component_spacing + dx_box_width // 2
        dx_frame = tk.Frame(display_canvas, bg='#F0F0F0', relief='solid', bd=1)
        dx_label = tk.Label(dx_frame, text="dx", font=('Arial', 12, 'bold'), 
                           bg='#F0F0F0', fg='#333333')
        dx_label.pack(padx=5, pady=2)
        display_canvas.create_window(dx_x, 110, window=dx_frame)
        
        # Equals sign position
        equals_x = start_x + integral_total_width + component_spacing + function_text_width + component_spacing + dx_box_width + component_spacing + equals_width // 2
        display_canvas.create_text(equals_x, 110, text="=", 
                                 font=('Arial', 20, 'bold'), fill='#333333')
        
        # Exact result string used for display; numeric shown in info below
        formatted_result = str(definite_result_exact)
        
        # Compute available result area and center x
        result_left_x = (start_x + integral_total_width + component_spacing +
                         function_text_width + component_spacing + dx_box_width +
                         component_spacing + equals_width + component_spacing)
        available_result_width = (total_width - right_margin) - result_left_x
        result_x = int(result_left_x + available_result_width / 2)
        
        # For definite integrals, convert any fractions to stacked format
        stacked_result, _ = self.convert_fractions_to_stacked(formatted_result)
        
        # Check if result contains fractions (has newlines)
        if '\n' in stacked_result:
            # For fractions, create a multi-line display with proper positioning
            lines = stacked_result.split('\n')
            
            # Calculate tighter vertical positioning for fractions
            # Reduce spacing between numerator, fraction bar, and denominator
            line_spacing = 15  # Reduced from 20 for tighter spacing
            fraction_height = len(lines) * line_spacing
            start_y = 110 - (fraction_height // 2) + 5  # Reduced offset for better centering
            
            # Display each line of the fraction with tighter spacing
            for i, line in enumerate(lines):
                y_offset = start_y + (i * line_spacing)
                display_canvas.create_text(result_x, y_offset, text=line, 
                                         font=('Arial', 16, 'bold'), fill='#333333')
        else:
            # Non-fraction: wrap to available width using font metrics
            font_obj = tkfont.Font(family='Arial', size=16, weight='bold')
            wrapped_lines = self.wrap_text_for_canvas(stacked_result, int(available_result_width), font_obj)
            line_spacing = int(font_obj.metrics('linespace') * 1.2) or 20
            start_y = int(110 - (len(wrapped_lines) - 1) * line_spacing / 2)
            for i, line in enumerate(wrapped_lines):
                y = start_y + i * line_spacing
                display_canvas.create_text(result_x, y, text=line,
                                           font=('Arial', 16, 'bold'), fill='#333333')
        
        # TeX label
        tex_label = tk.Label(main_frame, text="TeX", 
                           font=('Arial', 8), bg='#F5F5DC', fg='#999999')
        tex_label.place(x=total_width-60, y=250)
        
        # Additional info
        if numeric_result is not None:
            approx_text = f" ≈ {numeric_result:.4f}"
        else:
            approx_text = ""
        info_text = f"∫ from {a_display} to {b_display} of {func_str} dx = {formatted_result}{approx_text}"
        info_label = tk.Label(main_frame, text=info_text, 
                             font=('Arial', 11), bg='#F5F5DC', fg='#666666')
        info_label.pack(pady=(15, 0))
        
        # Close button
        close_btn = tk.Button(main_frame, text="Close", font=('Arial', 10, 'bold'),
                            bg='#4169E1', fg='white', relief='raised', bd=1,
                            command=result_window.destroy)
        close_btn.pack(pady=(15, 0))

def main():
    root = tk.Tk()
    app = IntegralCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
