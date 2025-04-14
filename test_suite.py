import unittest
from google_search_test import GoogleSearchTest
from example_test_case import ExampleDomainTest
from oncore_performance_test import OncorePerformanceTest


def create_test_suite():
    """Create a test suite with all test cases"""
    
    # Create a test suite
    test_suite = unittest.TestSuite()
    
    # Add tests to the suite using unittest.TestLoader
    loader = unittest.TestLoader()
    # test_suite.addTests(loader.loadTestsFromTestCase(ExampleDomainTest))
    # test_suite.addTests(loader.loadTestsFromTestCase(GoogleSearchTest))
    test_suite.addTests(loader.loadTestsFromTestCase(OncorePerformanceTest))
    
    return test_suite


if __name__ == "__main__":
    # Create the test suite
    suite = create_test_suite()
    
    # Create a test runner
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Run the test suite
    runner.run(suite)