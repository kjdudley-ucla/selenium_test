from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random


class GooglePage:
    """Page object representing Google search page"""
    
    # Locators
    SEARCH_BOX = (By.NAME, "q")
    SEARCH_RESULTS = (By.CSS_SELECTOR, "#search")  # More general selector
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
    
    def navigate(self):
        """Navigate to Google homepage"""
        try:
            self.driver.get("https://www.google.com")
            return self
        except Exception as e:
            print(f"Failed to navigate to Google: {e}")
            raise
    
    def wait_for_page_load(self):
        """Wait for the page to load completely"""
        try:
            self.wait.until(EC.visibility_of_element_located(self.SEARCH_BOX))
            # Add a small human-like delay
            time.sleep(random.uniform(0.5, 2))
            return self
        except Exception as e:
            print(f"Failed while waiting for page to load: {e}")
            raise
    
    def search(self, query):
        """Perform a search using the provided query"""
        try:
            search_input = self.driver.find_element(*self.SEARCH_BOX)
            search_input.clear()
            
            # Type like a human with random pauses
            for char in query:
                search_input.send_keys(char)
                time.sleep(random.uniform(0.05, 0.2))
                
            # Small pause before submitting
            time.sleep(random.uniform(0.5, 1.5))
            search_input.submit()
            
            # Wait for search results
            self.wait.until(EC.presence_of_element_located(self.SEARCH_RESULTS))
            return self
        except Exception as e:
            print(f"Failed during search operation: {e}")
            self.driver.save_screenshot("search_error.png")
            raise
    
    def take_screenshot(self, filename):
        """Take a screenshot of the current page"""
        try:
            self.driver.save_screenshot(filename)
            return self
        except Exception as e:
            print(f"Failed to take screenshot: {e}")
            raise
        
    def get_page_source(self):
        """Get the page source"""
        return self.driver.page_source