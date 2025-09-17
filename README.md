# Integral Calculator & Visualizer

A comprehensive desktop GUI application for calculating and visualizing integrals, built with Python, Tkinter, and Matplotlib.

## 📁 Project Structure

```
Integral_Caculator_Visualizer/
├── integral_calculator.py    # Main application file
├── run_calculator.py         # Launcher script with dependency checking
├── requirements.txt          # Python package dependencies
└── README.md                 # This documentation file
```

## 🚀 Features

- **Dual Integral Types**: Calculate both definite and indefinite integrals
- **Interactive GUI**: User-friendly desktop interface with Tkinter
- **Function Visualization**: Real-time plotting with Matplotlib
- **Symbolic Math**: Powered by SymPy for accurate symbolic calculations
- **LaTeX Output**: Mathematical expressions displayed in LaTeX format
- **Error Handling**: Robust input validation and error messages
- **Help System**: Built-in help for function syntax
- **Area Visualization**: Visual representation of definite integral areas

## 📋 Supported Functions

### Basic Operations
- Addition: `x + 2`
- Subtraction: `x - 3`
- Multiplication: `2*x` or `2x`
- Division: `x/2`
- Power: `x^2` or `x**2`

### Mathematical Functions
- **Trigonometric**: `sin(x)`, `cos(x)`, `tan(x)`, `sinh(x)`, `cosh(x)`, `tanh(x)`
- **Exponential/Logarithmic**: `exp(x)`, `log(x)`, `ln(x)`
- **Other**: `sqrt(x)`, `abs(x)`, `pi`, `e`

### Function Examples
- `x^2 + 3*x + 1` - Quadratic polynomial
- `sin(x) + cos(x)` - Trigonometric function
- `exp(x) * x` - Exponential function
- `1/(x^2 + 1)` - Rational function
- `sqrt(x^2 + 1)` - Square root function

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation Steps
1. **Clone or download this repository**
2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Dependencies
- `sympy>=1.12` - Symbolic mathematics library
- `matplotlib>=3.7.0` - Plotting and visualization
- `numpy>=1.24.0` - Numerical computing

## 🎯 Usage

### Quick Start (Recommended)
```bash
python run_calculator.py
```
*This launcher checks dependencies and provides helpful error messages*

### Direct Launch
```bash
python integral_calculator.py
```

## 🖥️ Application Interface

### Main Components
1. **Function Input Section**
   - Text field for mathematical expressions
   - Help button with syntax examples
   - Integral type selection (Definite/Indefinite)

2. **Bounds Input** (Definite Integrals Only)
   - Lower bound entry field
   - Upper bound entry field

3. **Control Buttons**
   - **Calculate Integral**: Computes the integral
   - **Plot Function**: Displays function graph
   - **Clear All**: Resets all inputs and results

4. **Results Display**
   - Scrollable text area
   - Shows function, integral result, and LaTeX format
   - Handles both definite and indefinite integrals

5. **Function Visualization**
   - Interactive matplotlib plot
   - Function graph with optional integral area shading
   - Zoom and pan capabilities
   - Grid and axis labels

## 🔧 Technical Architecture

### Core Components
- **`IntegralCalculator` Class**: Main application controller
- **GUI Framework**: Tkinter for cross-platform desktop interface
- **Mathematical Engine**: SymPy for symbolic mathematics
- **Visualization**: Matplotlib embedded in Tkinter canvas
- **Input Processing**: Regex-based function parsing and validation

### Key Methods
- `parse_function()`: Converts string input to SymPy expressions
- `calculate_integral()`: Performs symbolic integration
- `plot_function()`: Creates matplotlib visualizations
- `toggle_bounds()`: Shows/hides bounds input based on integral type

## ⚠️ Error Handling

The application includes comprehensive error handling for:
- **Invalid Function Syntax**: Clear error messages for malformed expressions
- **Mathematical Domain Errors**: Handles division by zero, undefined functions
- **Missing Input Validation**: Prevents calculation with empty fields
- **Plotting Errors**: Graceful handling of visualization issues
- **Dependency Checking**: Automatic verification of required packages

## 🎨 Visual Features

### Plot Capabilities
- **Function Graphing**: Smooth curves with customizable styling
- **Area Visualization**: Shaded regions for definite integrals
- **Boundary Lines**: Vertical lines marking integration bounds
- **Interactive Controls**: Zoom, pan, and legend
- **Multiple Functions**: Support for plotting multiple expressions

### Styling
- Modern, clean interface design
- Consistent color scheme
- Responsive layout
- Professional mathematical typography

## 🔮 Future Enhancements

### Planned Features
- **Multiple Function Plotting**: Compare multiple functions simultaneously
- **Step-by-Step Solutions**: Detailed integration process display
- **Export Functionality**: Save plots and results to files
- **Customizable Settings**: Adjustable plot ranges and styling
- **Advanced Functions**: Support for more complex mathematical functions
- **History Feature**: Save and recall previous calculations
- **3D Visualization**: Support for multivariable functions

### Potential Improvements
- **Performance Optimization**: Faster calculation for complex functions
- **Mobile Support**: Responsive design for different screen sizes
- **Plugin System**: Extensible architecture for custom functions
- **Cloud Integration**: Online storage and sharing capabilities

## 📝 Development Notes

### Code Organization
- **Modular Design**: Separate concerns for GUI, math, and visualization
- **Error Recovery**: Graceful handling of edge cases
- **User Experience**: Intuitive interface with helpful feedback
- **Extensibility**: Easy to add new features and functions

### Testing Recommendations
- Test with various function types (polynomials, trigonometric, exponential)
- Verify error handling with invalid inputs
- Check visualization accuracy for known integrals
- Test on different operating systems and Python versions
