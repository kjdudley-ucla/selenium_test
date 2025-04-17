from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import os
from datetime import datetime


class OncorePage:
    """Page object representing OnCore application pages"""
    
    # Common locators
    ARM_SELECTOR = (By.ID, "arm_selector")
    CLOSE_BUTTON = (By.LINK_TEXT, "Close")
    SUBMIT_BUTTON = (By.NAME, "submit1")
    
    # Login locators
    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    NEXT_BUTTON = (By.ID, "submitBtn")
    LOGIN_BUTTON = (By.NAME, "submitBtn")
    
    # Tab locators
    PROTOCOL_TAB = (By.XPATH, "//a[contains(text(),'Protocol')]")
    MANAGEMENT_TAB = (By.XPATH, "//a[contains(text(),'Management')]")
    STAFF_TAB = (By.XPATH, "//a[contains(text(),'Staff')]")
    REVIEWS_TAB = (By.CSS_SELECTOR, "tr:nth-child(7) > .oMTab")
    ANNOTATIONS_TAB = (By.CSS_SELECTOR, "tr:nth-child(12) > .oMTab")
    ON_STUDY_TAB = (By.CSS_SELECTOR, "tr:nth-child(5) > .oMTab")
    DEVIATIONS_TAB = (By.CSS_SELECTOR, "tr:nth-child(8) > .oMTab")
    INVOICABLE_ITEMS_TAB = (By.CSS_SELECTOR, "tr:nth-child(9) > .oMTab")
    
    # Link locators
    CRA_CONSOLE_LINK = (By.LINK_TEXT, "CRA Console")
    COV_ANALYSIS_LINK = (By.LINK_TEXT, "Coverage Analysis Console")
    FINANCIALS_LINK = (By.LINK_TEXT, "Financials Console")
    SPECIFICATIONS_LINK = (By.LINK_TEXT, "Specifications")
    PHYSICAL_EXAM_LINK = (By.LINK_TEXT, "Physical Exam")
    
    def __init__(self, driver, base_url="https://crmsdev.mednet.ucla.edu", iteration=1):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(self.driver, 10)
        self.performance_data = []
        self.iteration = iteration
        
    def navigate_to(self, endpoint):
        """Navigate to a specific URL endpoint"""
        full_url = f"{self.base_url}{endpoint}" if not endpoint.startswith("http") else endpoint
        self.driver.get(full_url)
        return self
    
    def wait_between_actions(self, seconds=5):
        """Wait between actions to give browser time to respond"""
        time.sleep(seconds)
        
    def wait_for_element(self, locator, timeout=30):
        """Wait for an element to be visible"""
        return self.wait.until(EC.visibility_of_element_located(locator))
    
    def wait_for_clickable(self, locator, timeout=30):
        """Wait for an element to be clickable"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    
    def click_element(self, locator):
        """Click an element after making sure it's clickable"""
        elem = self.wait_for_clickable(locator)
        elem.click()
        # Add pause after clicking to let the browser catch up
        self.wait_between_actions()
        return self
    
    def measure_page_load(self, page_name):
        """Measure page load time and add to performance data"""
        # Execute JavaScript to get performance metrics
        load_time = self.driver.execute_script(
            "return window.performance.getEntriesByType('navigation')[0].duration;"
        )
        
        # Record performance data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.performance_data.append({
            'timestamp': timestamp,
            'page': page_name,
            'load_time_ms': load_time,
            'iteration': self.iteration
        })
        
        # Print the result for immediate feedback
        print(f"Iteration {self.iteration} - {page_name}: {load_time} ms")
        
        # Add pause after measuring to let the browser catch up
        self.wait_between_actions()
        
        return load_time
    
    def save_performance_data(self, filename="oncore_performance.csv"):
        """Save the collected performance data to a CSV file"""
        if not self.performance_data:
            print("No performance data to save.")
            return
            
        # Check if the file already exists
        file_exists = os.path.isfile(filename)
        
        # Open in append mode if file exists, otherwise in write mode
        with open(filename, 'a' if file_exists else 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'page', 'load_time_ms', 'iteration']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Only write the header if we're creating a new file
            if not file_exists:
                writer.writeheader()
                
            for data in self.performance_data:
                writer.writerow(data)
                
        print(f"Performance data saved to {filename}")
        return self
    
    def execute_script(self, script):
        """Execute JavaScript in the browser"""
        result = self.driver.execute_script(script)
        # Add pause after script execution to let the browser catch up
        self.wait_between_actions()
        return result
    
    def select_arm(self, arm_label):
        """Select an arm from the dropdown"""
        self.wait_for_element(self.ARM_SELECTOR)
        self.driver.find_element(*self.ARM_SELECTOR).click()
        self.wait_between_actions(2)  # Shorter wait after click before selecting option
        
        # Create a selector for the specific option
        option_selector = (By.XPATH, f"//option[contains(text(),'{arm_label}')]")
        self.wait_for_element(option_selector).click()
        self.wait_between_actions()
        
        return self
    
    def handle_new_window(self):
        """Switch to new window when opened"""
        # Store the current window handle
        original_window = self.driver.current_window_handle
        
        # Wait for the new window to open and switch to it
        self.wait.until(EC.number_of_windows_to_be(2))
        
        # Switch to the new window
        for window_handle in self.driver.window_handles:
            if window_handle != original_window:
                self.driver.switch_to.window(window_handle)
                break
        
        self.wait_between_actions()
        return original_window
    
    def close_and_return(self, original_window):
        """Close current window and switch back to original"""
        self.driver.close()
        self.driver.switch_to.window(original_window)
        self.wait_between_actions()
        return self
        
    def login(self, username, password):
        """Login to OnCore application with two-step authentication"""
        # Enter username and click Next
        print("Entering username and clicking Next...")
        try:
            username_field = self.wait_for_element(self.USERNAME_FIELD)
            username_field.clear()
            username_field.send_keys(username)
            self.wait_between_actions(2)  # Wait before clicking next
            self.click_element(self.NEXT_BUTTON)
            self.measure_page_load("UsernameEntryStep")
            
            # Enter password and click Login
            print("Entering password and clicking Login...")
            password_field = self.wait_for_element(self.PASSWORD_FIELD)
            password_field.clear()
            password_field.send_keys(password)
            self.wait_between_actions(2)  # Wait before clicking login
            self.click_element(self.LOGIN_BUTTON)
            self.measure_page_load("LoginComplete")
            
            # Verify login was successful by checking for login error messages or expected post-login elements
            # Wait a short time to see if we land on the expected page
            self.wait_between_actions(10)
            
            # Check for error messages or if we're still on the login page
            if "login" in self.driver.current_url.lower():
                # Look for common error elements that might indicate login failure
                error_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Invalid') or contains(text(), 'Failed') or contains(text(), 'error')]")
                if error_elements:
                    error_msg = error_elements[0].text
                    print(f"Login failed: {error_msg}")
                    raise Exception(f"Login failed: {error_msg}")
                else:
                    print("Login failed: Still on login page after authentication attempt")
                    raise Exception("Login failed: Still on login page after authentication attempt")
        except Exception as e:
            print(f"Error during login: {str(e)}")
            raise Exception(f"Login failed: {str(e)}")
        
        return self