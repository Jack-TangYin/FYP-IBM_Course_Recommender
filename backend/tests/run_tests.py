#!/usr/bin/env python3
"""
Test runner for the course recommender system
Runs all test suites and generates coverage report
"""

import unittest
import coverage
import os
import sys

def run_tests_with_coverage():
    """Run all tests with coverage tracking"""
    # Start coverage measurement
    cov = coverage.Coverage(
        source=['backend'],  # Updated to target the backend directory
        omit=['*tests*', '*venv*', '*gradio*'],
    )
    cov.start()
    
    # Discover and run all tests
    test_loader = unittest.TestLoader()
    # This line has the issue - we're fixing the path
    test_dir = os.path.dirname(os.path.abspath(__file__))  # Points to current directory (tests)
    test_suite = test_loader.discover(test_dir, pattern='*_tests.py')
    
    # Run the tests
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Stop coverage measurement
    cov.stop()
    cov.save()
    
    # Print coverage report
    print("\nCoverage Report:")
    cov.report()
    
    # Generate HTML report
    html_dir = os.path.join(os.path.dirname(test_dir), 'htmlcov')
    cov.html_report(directory=html_dir)
    print(f"\nHTML coverage report generated in: {html_dir}")
    
    return result

if __name__ == '__main__':
    # Make sure the module can be imported
    # This adds the parent directory of the test directory to the path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    print("Running all test suites for IBM Course Recommender System")
    result = run_tests_with_coverage()
    
    # Exit with appropriate status code
    sys.exit(not result.wasSuccessful())