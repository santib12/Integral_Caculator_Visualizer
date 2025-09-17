#!/usr/bin/env python3
"""
Test runner for the Integral Calculator & Visualizer
Runs all test suites and generates reports.
"""

import sys
import os
import subprocess

def run_test_file(test_file):
    """Run a single test file and return the result"""
    print(f"\n{'='*60}")
    print(f"Running: {test_file}")
    print('='*60)
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("[OK] PASSED")
            print(result.stdout)
        else:
            print("[ERROR] FAILED")
            print(result.stderr)
            
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("[TIMEOUT] TIMEOUT")
        return False
    except Exception as e:
        print(f"[ERROR] ERROR: {e}")
        return False

def main():
    """Run all test suites"""
    print("INTEGRAL CALCULATOR TEST SUITE")
    print("="*60)
    
    # Test files to run
    test_files = [
        "tests/test_final_accuracy.py",
        "tests/test_definite_integrals.py", 
        "tests/test_definite_formatting.py",
        "tests/test_improved_accuracy.py",
        "tests/test_integrals.py",
        "tests/test_complex_integrals.py",
        "tests/test_advanced_mathematics.py",
        "tests/test_comprehensive_integrals.py",
        "tests/test_advanced_scenarios.py"
    ]
    
    # Check if test files exist
    existing_tests = []
    for test_file in test_files:
        if os.path.exists(test_file):
            existing_tests.append(test_file)
        else:
            print(f"[WARN] Test file not found: {test_file}")
    
    if not existing_tests:
        print("[ERROR] No test files found!")
        return
    
    # Run tests
    passed = 0
    total = len(existing_tests)
    
    for test_file in existing_tests:
        if run_test_file(test_file):
            passed += 1
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("ALL TESTS PASSED!")
        print("The integral calculator is ready for production use.")
    else:
        print("Some tests failed. Please review the output above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
