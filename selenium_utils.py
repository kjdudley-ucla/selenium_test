from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os
import datetime


class SeleniumUtils:
    """Utility class for common Selenium operations"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.actions = ActionChains(self.driver)
    
    def wait_for_element(self, locator, timeout=10):
        """Wait for an element to be present and visible"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))
    
    def wait_for_clickable(self, locator, timeout=10):
        """Wait for an element to be clickable"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    
    def safe_click(self, locator, timeout=10):
        """Safely click on an element after ensuring it's clickable"""
        element = self.wait_for_clickable(locator, timeout)
        element.click()
        return element
    
    def take_timestamped_screenshot(self, prefix="screenshot"):
        """Take a screenshot with a timestamp in the filename"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshots_dir = "screenshots"
        
        # Create screenshots directory if it doesn't exist
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
        
        # Generate the filename with timestamp
        filename = f"{screenshots_dir}/{prefix}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        return filename
    
    def scroll_to_element(self, element):
        """Scroll to an element to make it visible"""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        return element
    
    def hover_over_element(self, element):
        """Hover over an element"""
        self.actions.move_to_element(element).perform()
        return element