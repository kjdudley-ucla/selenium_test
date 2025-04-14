from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ExamplePage:
    """Page object representing Example.com page"""
    
    # Locators
    HEADER = (By.TAG_NAME, "h1")
    PARAGRAPH = (By.TAG_NAME, "p")
    MORE_INFO_LINK = (By.XPATH, "//a[contains(text(), 'More information')]")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
    
    def navigate(self):
        """Navigate to Example.com homepage"""
        self.driver.get("https://www.example.com")
        return self
    
    def wait_for_page_load(self):
        """Wait for the page to load completely"""
        self.wait.until(EC.visibility_of_element_located(self.HEADER))
        return self
    
    def get_header_text(self):
        """Get the text from the main header"""
        return self.driver.find_element(*self.HEADER).text
    
    def get_paragraph_text(self):
        """Get the text from the main paragraph"""
        return self.driver.find_element(*self.PARAGRAPH).text
    
    def has_more_info_link(self):
        """Check if the 'More information' link exists"""
        elements = self.driver.find_elements(*self.MORE_INFO_LINK)
        return len(elements) > 0
    
    def take_screenshot(self, filename):
        """Take a screenshot of the current page"""
        self.driver.save_screenshot(filename)
        return self
        
    def get_page_source(self):
        """Get the page source"""
        return self.driver.page_source