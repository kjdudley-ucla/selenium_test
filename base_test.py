from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import unittest


class BaseTest(unittest.TestCase):
    """Base test class for all Selenium tests"""
    
    def setUp(self):
        """Set up test environment before each test method runs"""
        print("Setting up the test environment...")
        
        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        # chrome_options.add_argument("--headless")  # Uncomment to run without UI
        
        # Add anti-bot detection evasion
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        
        # Set up Chrome driver with automatic webdriver management
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Mask WebDriver to avoid detection
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        self.driver.implicitly_wait(10)  # Set implicit wait
    
    def tearDown(self):
        """Clean up test environment after each test method runs"""
        print("Tearing down the test environment...")
        if self.driver:
            self.driver.quit()