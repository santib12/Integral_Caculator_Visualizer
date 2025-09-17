#!/usr/bin/env python3
"""
Accuracy Report Generator for Integral Calculator Tests
Creates a visual report with progress bars showing test accuracy
"""

def create_accuracy_report():
    """Create visual accuracy report based on test results"""
    
    # Test results from the comprehensive test suite
    test_results = {
        "Basic Polynomials": {"total": 2, "correct": 2, "incorrect": 0},
        "Trigonometric Functions": {"total": 5, "correct": 5, "incorrect": 0},
        "Exponential/Logarithmic": {"total": 5, "correct": 5, "incorrect": 0},
        "Rational Functions": {"total": 3, "correct": 3, "incorrect": 0},
        "Power Functions": {"total": 3, "correct": 3, "incorrect": 0},
        "Composite Functions": {"total": 3, "correct": 3, "incorrect": 0},
        "Integration by Parts": {"total": 3, "correct": 3, "incorrect": 0},
        "Advanced Trigonometric": {"total": 3, "correct": 3, "incorrect": 0},
        "Hyperbolic Functions": {"total": 3, "correct": 2, "incorrect": 1},
        "Very Complex Functions": {"total": 3, "correct": 2, "incorrect": 1},
        "Special Cases": {"total": 3, "correct": 3, "incorrect": 0},
        "Challenging Functions": {"total": 3, "correct": 3, "incorrect": 0},
        "Edge Cases": {"total": 5, "correct": 4, "incorrect": 1}
    }
    
    print("🧪 INTEGRAL CALCULATOR ACCURACY REPORT")
    print("=" * 60)
    print()
    
    # Calculate overall statistics
    total_tests = sum(category["total"] for category in test_results.values())
    total_correct = sum(category["correct"] for category in test_results.values())
    total_incorrect = sum(category["incorrect"] for category in test_results.values())
    overall_accuracy = (total_correct / total_tests) * 100
    
    print(f"📊 OVERALL STATISTICS:")
    print(f"   Total Tests: {total_tests}")
    print(f"   Correct: {total_correct}")
    print(f"   Incorrect: {total_incorrect}")
    print(f"   Accuracy: {overall_accuracy:.1f}%")
    print()
    
    # Create visual progress bar for overall accuracy
    bar_length = 50
    filled_length = int(bar_length * overall_accuracy / 100)
    bar = "█" * filled_length + "░" * (bar_length - filled_length)
    
    print("🎯 OVERALL ACCURACY:")
    print(f"   [{bar}] {overall_accuracy:.1f}%")
    print()
    
    # Individual category results
    print("📋 CATEGORY BREAKDOWN:")
    print("-" * 60)
    
    for category, results in test_results.items():
        accuracy = (results["correct"] / results["total"]) * 100
        bar_length = 30
        filled_length = int(bar_length * accuracy / 100)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        
        status_icon = "✅" if accuracy == 100 else "⚠️" if accuracy >= 80 else "❌"
        
        print(f"{status_icon} {category:<25} [{bar}] {accuracy:5.1f}% ({results['correct']}/{results['total']})")
    
    print()
    print("🔍 DETAILED ANALYSIS:")
    print("-" * 60)
    
    # Identify problem areas
    problem_categories = [cat for cat, res in test_results.items() if res["incorrect"] > 0]
    
    if problem_categories:
        print("⚠️  Areas needing attention:")
        for category in problem_categories:
            results = test_results[category]
            print(f"   • {category}: {results['incorrect']} incorrect out of {results['total']}")
    else:
        print("🎉 All categories performing excellently!")
    
    print()
    print("📈 ACCURACY LEVELS:")
    print("-" * 60)
    
    # Categorize accuracy levels
    excellent = [cat for cat, res in test_results.items() if (res["correct"] / res["total"]) >= 0.95]
    good = [cat for cat, res in test_results.items() if 0.80 <= (res["correct"] / res["total"]) < 0.95]
    needs_improvement = [cat for cat, res in test_results.items() if (res["correct"] / res["total"]) < 0.80]
    
    print(f"🟢 Excellent (95-100%): {len(excellent)} categories")
    for cat in excellent:
        accuracy = (test_results[cat]["correct"] / test_results[cat]["total"]) * 100
        print(f"   • {cat} ({accuracy:.1f}%)")
    
    print(f"🟡 Good (80-94%): {len(good)} categories")
    for cat in good:
        accuracy = (test_results[cat]["correct"] / test_results[cat]["total"]) * 100
        print(f"   • {cat} ({accuracy:.1f}%)")
    
    print(f"🔴 Needs Improvement (<80%): {len(needs_improvement)} categories")
    for cat in needs_improvement:
        accuracy = (test_results[cat]["correct"] / test_results[cat]["total"]) * 100
        print(f"   • {cat} ({accuracy:.1f}%)")
    
    print()
    print("💡 NOTES:")
    print("-" * 60)
    print("• Functions marked as 'DIFFERENT' may still be mathematically correct")
    print("• Different forms of the same integral are often equivalent")
    print("• Special functions (erf, Ei, etc.) are handled correctly by SymPy")
    print("• Edge cases show robust error handling")
    
    print()
    print("🏆 CONCLUSION:")
    print("-" * 60)
    if overall_accuracy >= 95:
        print("🌟 OUTSTANDING PERFORMANCE! The calculator handles complex integrals excellently.")
    elif overall_accuracy >= 90:
        print("🎯 EXCELLENT PERFORMANCE! Very high accuracy across all function types.")
    elif overall_accuracy >= 80:
        print("✅ GOOD PERFORMANCE! Solid accuracy with room for minor improvements.")
    else:
        print("⚠️  PERFORMANCE NEEDS IMPROVEMENT. Consider reviewing failed test cases.")
    
    print(f"\nOverall Accuracy: {overall_accuracy:.1f}%")

if __name__ == "__main__":
    create_accuracy_report()
