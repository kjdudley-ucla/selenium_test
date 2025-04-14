from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random


def setup_driver():
    """Set up and return a Chrome WebDriver instance."""
    # Configure Chrome options
    chrome_options = Options()
    # Uncomment the line below to run in headless mode (no browser UI)
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    
    # Add anti-bot detection evasion
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    # Set up Chrome driver with automatic webdriver management
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Mask WebDriver to avoid detection
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver


def run_test():
    """Run a simple website test using Selenium."""
    driver = setup_driver()
    try:
        # Navigate to a website
        print("Navigating to the test website...")
        driver.get("https://www.google.com")
        
        # Wait for the page to load completely
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        print("Page loaded successfully!")
        
        # Add a small random delay to mimic human interaction
        time.sleep(random.uniform(1, 3))
        
        # Find the search box and enter a query
        search_box.send_keys("Selenium Python testing")
        
        # Add another small delay before submission
        time.sleep(random.uniform(0.5, 2))
        
        # Submit the form
        search_box.submit()
        print("Search query submitted!")
        
        # Wait for search results to load - using a very general selector
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#search"))
        )
        print("Search results loaded!")
        
        # Take a screenshot
        driver.save_screenshot("search_results.png")
        print("Screenshot taken and saved as 'search_results.png'")
        
        # Pause to see the results
        time.sleep(3)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot("error_screenshot.png")
        print("Error screenshot saved as 'error_screenshot.png'")
        
    finally:
        # Always close the browser, even if there are exceptions
        print("Closing the browser...")
        driver.quit()


if __name__ == "__main__":
    run_test()