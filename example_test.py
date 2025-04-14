from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def setup_driver():
    """Set up and return a Chrome WebDriver instance."""
    # Configure Chrome options
    chrome_options = Options()
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


def run_example_test():
    """Run a simple test on example.com."""
    driver = setup_driver()
    try:
        # Navigate to example.com - a simple and stable test site
        print("Navigating to example.com...")
        driver.get("https://www.example.com")
        
        # Wait for the page to load
        header = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        print(f"Page loaded successfully! Page title: {driver.title}")
        print(f"Header text: {header.text}")
        
        # Check if expected text is present
        if "Example Domain" in driver.page_source:
            print("✓ Verified: 'Example Domain' text is present on the page")
        else:
            print("✗ Verification failed: 'Example Domain' text not found")
        
        # Take a screenshot
        driver.save_screenshot("example_site.png")
        print("Screenshot taken and saved as 'example_site.png'")
        
        # Pause to see the results
        time.sleep(2)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot("error_screenshot.png")
        print("Error screenshot saved as 'error_screenshot.png'")
        
    finally:
        # Always close the browser, even if there are exceptions
        print("Closing the browser...")
        driver.quit()


if __name__ == "__main__":
    run_example_test()