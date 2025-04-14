from base_test import BaseTest
from page_objects.google_page import GooglePage
import time
import unittest


class GoogleSearchTest(BaseTest):
    """Test case for Google search functionality using Page Object Model"""
    
    def test_google_search(self):
        """Test performing a search on Google"""
        # Initialize the Google page object
        google_page = GooglePage(self.driver)
        
        # Navigate to Google and perform a search
        google_page.navigate().wait_for_page_load().search("Selenium Python automation")
        
        # Take a screenshot of the results
        google_page.take_screenshot("google_search_results.png")
        
        # Verify that search results contain the expected text
        page_source = google_page.get_page_source()
        self.assertIn("Selenium", page_source, "Search results should contain 'Selenium'")
        
        # Pause briefly to see the results (you might want to remove this in production)
        time.sleep(2)


if __name__ == "__main__":
    unittest.main()