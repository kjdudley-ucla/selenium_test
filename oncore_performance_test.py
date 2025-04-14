from base_test import BaseTest
from page_objects.oncore_page import OncorePage
import unittest
import time
import getpass
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException


class OncorePerformanceTest(BaseTest):
    """Test case for OnCore performance testing using Page Object Model"""
    
    base_url = None
    username = None
    password = None
    
    @classmethod
    def setUpClass(cls):
        """Setup that runs once before all tests"""
        super().setUpClass()
        # Prompt for the testing environment URL
        cls.base_url = input("Enter the OnCore environment URL (e.g., https://crmsdev.mednet.ucla.edu): ")
        if not cls.base_url.startswith("http"):
            cls.base_url = "https://" + cls.base_url
        print(f"Using environment: {cls.base_url}")
        
        # Prompt for login credentials once
        cls.username = input("Enter your OnCore username: ")
        cls.password = getpass.getpass("Enter your OnCore password: ")
        print("Credentials stored for all test methods")    
        
    def test_protocol_performance(self):
        """Test the performance of the 16-000265 protocol in OnCore"""
        # Use credentials stored in setUpClass
        username, password = self.__class__.username, self.__class__.password
        
        # Initialize the OnCore page object
        oncore_page = OncorePage(self.driver)
        
        # Navigate to the login page
        print("Loading login page...")
        oncore_page.navigate_to(self.base_url)
        oncore_page.measure_page_load("LoginPage")
        
        # Login with username and password, exit on failure
        try:
            oncore_page.login(username, password)
            
        except Exception as e:
            print(f"Login failed: {str(e)}")
            print("Exiting test due to login failure.")
            import sys
            sys.exit(1)  # Exit with error status code
          # Protocol Information Page
        print("Loading Protocol Information page...")
        oncore_page.navigate_to(
            f"{self.base_url}/smrs/PRControlServlet?hdn_function=PROTOCOL_INQUIRY&hdn_function_type=INQUIRY&protocol_id=797&protocol_no=16-000265&console=PC"
        )
        oncore_page.wait_between_actions()  # Wait after navigation
        oncore_page.measure_page_load("16-000265Protocol")
          # Management Tab
        print("Loading Management tab...")
        oncore_page.navigate_to(
            f"{self.base_url}/smrs/PRControlServlet?hdn_function=PROTOCOL_DETAILS&hdn_function_type=INQUIRY&protocol_id=797&protocol_no=16-000265&console=PC"
        )
        oncore_page.wait_between_actions()  # Wait after navigation
        oncore_page.measure_page_load("16-000265Mgmt")
          # Staff Tab
        print("Loading Staff tab...")
        oncore_page.navigate_to(
            f"{self.base_url}/smrs/PRControlServlet?hdn_function=PROTOCOL_STAFF&hdn_function_type=INQUIRY&protocol_id=797&protocol_no=16-000265&console=PC"
        )
        oncore_page.wait_between_actions()  # Wait after navigation
        oncore_page.measure_page_load("16-000265Staff")
          # Reviews Tab
        print("Loading Reviews tab...")
        oncore_page.navigate_to(
            f"{self.base_url}/smrs/PRControlServlet?hdn_function=PROTOCOL_REVIEWS&hdn_function_type=INQUIRY&protocol_id=797&protocol_no=16-000265&console=PC"
        )
        oncore_page.wait_between_actions()  # Wait after navigation
        oncore_page.measure_page_load("16-000265Reviews")
          # Annotations Tab
        print("Loading Annotations tab...")
        oncore_page.navigate_to(
            f"{self.base_url}/smrs/PRControlServlet?hdn_function=ANNOTATION_INQUIRY&hdn_function_type=INQUIRY&protocol_id=797&protocol_no=16-000265&console=PC"
        )
        oncore_page.wait_between_actions()  # Wait after navigation
        oncore_page.measure_page_load("16-000265Annotations")
          # CRA Console
        print("Loading CRA Console...")
        oncore_page.navigate_to(
            f"{self.base_url}/smrs/SMRSControlServlet?hdn_function=CRA_CONSOLE"
        )
        oncore_page.wait_between_actions()  # Wait after navigation
        oncore_page.measure_page_load("16-000265CRA")
          # Subject Visit
        print("Loading Subject Visit...")
        oncore_page.navigate_to(
            f"{self.base_url}/smrs/SubjectStudyDataControlServlet?hdn_function=SUBJECT_INQUIRY&hdn_function_type=VIEW_ALL&protocol_subject_id=4350&console=SUBJECT-CONSOLE"
        )
        oncore_page.wait_between_actions()  # Wait after navigation
        oncore_page.measure_page_load("16-000265SubjectVisit")
        
        # Calendar Tab
        print("Opening Calendar Tab...")
        oncore_page.execute_script("setActiveTab('SUBJECT_CALENDAR')")
        oncore_page.wait_between_actions()  # Wait after script execution
        oncore_page.measure_page_load("16-000265Calendar")
        
        # On Study Tab
        print("Opening On Study Tab...")
        oncore_page.execute_script("setActiveTab('SUBJECT_ONSTUDY')")
        oncore_page.wait_between_actions()  # Wait after script execution
        oncore_page.measure_page_load("16-000265OnStudy")
          # Return to CRA Console
        print("Returning to CRA Console...")
        oncore_page.navigate_to(
            f"{self.base_url}/smrs/SMRSControlServlet?hdn_function=CRA_CONSOLE"
        )
        oncore_page.wait_between_actions()  # Wait after navigation
        oncore_page.measure_page_load("16-000265CRA2")
        
        # SAEs Tab via JavaScript
        print("Opening SAEs Tab...")
        oncore_page.execute_script("setTab('TOXICITIES', 'TOXICITIES')")
        oncore_page.wait_between_actions()  # Wait after script execution
        oncore_page.measure_page_load("16-000265SAE")
        
        # Deviations Tab
        print("Opening Deviations Tab...")
        oncore_page.click_element((By.CSS_SELECTOR, "tr:nth-child(8) > .oMTab"))
        oncore_page.wait_between_actions()  # Wait after click
        oncore_page.measure_page_load("16-000265Deviations")
          # Coverage Analysis
        print("Opening Coverage Analysis...")
        oncore_page.navigate_to(
            f"{self.base_url}/smrs/coverageAnalysisConsole/protocolSummary/details.do"
        )
        oncore_page.wait_between_actions()  # Wait after navigation
        oncore_page.measure_page_load("16-000265CovA")
          # Procedures
        print("Opening Procedures...")
        oncore_page.navigate_to(f"{self.base_url}/smrs/coverageAnalysisConsole/procedures/all.do")
        oncore_page.wait_between_actions()  # Wait after navigation
        oncore_page.measure_page_load("16-000265Proc")
        
        # Physical Exam
        print("Opening Physical Exam...")
        link = WebDriverWait(oncore_page.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'javascript:toProcedureDetails')]")))
        link.click()  # Click the link to open Physical Exam procedure
        oncore_page.wait_between_actions()  # Wait after click
        oncore_page.measure_page_load("16-000265PhysEx")
          # Billing Grid
        print("Opening Billing Grid...")
        oncore_page.navigate_to(f"{self.base_url}/smrs/coverageAnalysisConsole/billingGrid/display.do")
        oncore_page.wait_between_actions()  # Wait after navigation
        oncore_page.measure_page_load("16-000265BG")
          # Financials Console
        print("Opening Financials Console...")
        oncore_page.navigate_to(
            f"{self.base_url}/smrs/SMRSControlServlet?hdn_function=PROTOCOL_BUDGET"
        )
        oncore_page.wait_between_actions()  # Wait after navigation
        oncore_page.measure_page_load("16-000265Financials")
        
        # Subject Related Tab
        print("Opening Subject Related Tab...")
        oncore_page.click_element((By.CSS_SELECTOR, "tr:nth-child(5) > .oMTab"))
        oncore_page.wait_between_actions()  # Wait after click
        oncore_page.measure_page_load("16-000265SubRel")
        
        # Physical Exam Procedure
        print("Opening Physical Exam Procedure...")
        link = WebDriverWait(oncore_page.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'javascript:toProcedureDetails')]")))
        link.click()  # Click the link to open Physical Exam procedure
        oncore_page.wait_between_actions()  # Wait after click
        oncore_page.measure_page_load("16-000265PhysEx2")
        
        # Close
        print("Closing dialog...")
        oncore_page.click_element(oncore_page.CLOSE_BUTTON)
        oncore_page.wait_between_actions()  # Wait after click
        
        # Invoicable Items Tab
        print("Opening Invoicable Items Tab...")
        oncore_page.click_element(oncore_page.INVOICABLE_ITEMS_TAB)
        oncore_page.wait_between_actions()  # Wait after click
        oncore_page.measure_page_load("16-000265Inv")
          # Specifications
        print("Opening Specifications...")
        oncore_page.navigate_to(
            f"{self.base_url}/smrs/SMRSControlServlet?hdn_function=STUDY_SETUP"
        )
        oncore_page.wait_between_actions()  # Wait after navigation
        oncore_page.measure_page_load("16-000265Spec")
        
        # Select Arm > BLD
        print("Selecting BLD arm...")
        arm_dropdown = oncore_page.driver.find_element(By.ID, "arm_selector")
        select = Select(arm_dropdown)
        select.select_by_visible_text("BLD")  # Select the "BLD" arm
        oncore_page.wait_between_actions()  # Wait after selection
        oncore_page.measure_page_load("16-000265SelectArm")
        
        # Open Physical Exam procedure from specifications
        print("Opening Physical Exam procedure...")
        link = WebDriverWait(oncore_page.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'javascript:toProcedureNotes')]")))
        link.click()  # Click the link to open Physical Exam procedure
        oncore_page.wait_between_actions()  # Wait after click
        oncore_page.measure_page_load("16-000265PhysEx3")
        
        # Wait for the page to be completely loaded
        WebDriverWait(oncore_page.driver, 10).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete'
        )
        oncore_page.wait_between_actions()  # Wait after page load

        # Store the current window handles before opening a new window
        print("Current window handles before opening new window:", self.driver.window_handles)
        current_window_handle = self.driver.current_window_handle
        print(f"Current window handle: {current_window_handle}")
        
        # Take a screenshot before attempting to open a new window
        self.driver.save_screenshot("before_opening_new_window.png")
        print("Screenshot saved before opening new window")

        # Open Visits (this will open in a new window)
        print("Opening Visits in new window...")
        try:
            # Execute the JavaScript to open the new window
            oncore_page.execute_script("browseFootNoteVisits('11683')")
            print("JavaScript executed to open new window")
            oncore_page.wait_between_actions(10)  # Increase wait time after script execution
            
            # Check if a new window was opened
            window_handles = self.driver.window_handles
            print(f"Window handles after executing script: {window_handles}")
            
            if len(window_handles) < 2:
                print("No new window detected. Taking screenshot...")
                self.driver.save_screenshot("no_new_window_opened.png")
                print("Will try to continue with the test on the current window")
                # Continue in the current window
            else:
                # Switch to the new window
                print("New window detected. Switching to it...")
                new_window = None
                for handle in window_handles:
                    if handle != current_window_handle:
                        new_window = handle
                        break
                
                if new_window:
                    print(f"Switching to new window: {new_window}")
                    self.driver.switch_to.window(new_window)
                    oncore_page.wait_between_actions()  # Wait after switching windows
                    
                    # Take a screenshot after switching to the new window
                    self.driver.save_screenshot("after_window_switch.png")
                    print("Screenshot saved after window switch")
                    
                    # Check the page title and URL for debugging
                    print(f"New window title: {self.driver.title}")
                    print(f"New window URL: {self.driver.current_url}")
                    
                    # Measure page load time
                    oncore_page.measure_page_load("16-000265Visits")
                    
                    # Look for the submit button with extra debugging
                    try:
                        print("Looking for submit button...")
                        # Check if the submit button exists
                        submit_buttons = self.driver.find_elements(By.NAME, "submit1")
                        if submit_buttons:
                            print(f"Found {len(submit_buttons)} submit buttons")
                            # Try using the standard click_element method with increased timeout
                            try:
                                print("Attempting to click submit button using click_element method")
                                wait = WebDriverWait(self.driver, 20)  # Increased timeout
                                submit_button = wait.until(EC.element_to_be_clickable(oncore_page.SUBMIT_BUTTON))
                                submit_button.click()
                                print("Submit button clicked successfully")
                                oncore_page.wait_between_actions()  # Wait after click
                                oncore_page.measure_page_load("16-000265Submit")
                            except TimeoutException:
                                print("TimeoutException occurred when trying to click submit button")
                                # Try alternative approach - click the first submit button directly
                                print("Trying alternative approach - direct click")
                                submit_buttons[0].click()
                                print("Submit button clicked directly")
                                oncore_page.wait_between_actions()  # Wait after click
                                oncore_page.measure_page_load("16-000265Submit")
                        else:
                            print("No submit buttons found in the new window")
                            # Try finding any button that might serve the same purpose
                            buttons = self.driver.find_elements(By.TAG_NAME, "button")
                            if buttons:
                                print(f"Found {len(buttons)} buttons, clicking the first one")
                                buttons[0].click()
                                print("Alternative button clicked")
                            else:
                                print("No buttons found either")
                    except Exception as e:
                        print(f"Error trying to interact with submit button: {str(e)}")
                        self.driver.save_screenshot("submit_button_error.png")
                    
                    # Close the window and return to original
                    print("Closing window and returning to original...")
                    try:
                        self.driver.close()
                        print("Window closed")
                    except Exception as e:
                        print(f"Error closing window: {str(e)}")
                    
                    # Switch back to the original window
                    print(f"Switching back to original window: {current_window_handle}")
                    self.driver.switch_to.window(current_window_handle)
                    oncore_page.wait_between_actions()  # Wait after switching windows
                    
                    # Take a screenshot after switching back to the original window
                    self.driver.save_screenshot("back_to_original_window.png")
                    print("Screenshot saved after returning to original window")
                else:
                    print("Could not identify the new window handle")
        except Exception as e:
            print(f"Error during window handling: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Try to recover by ensuring we're on the original window
            try:
                print("Attempting to recover by switching back to original window")
                self.driver.switch_to.window(current_window_handle)
                print("Successfully switched back to original window")
            except Exception as e2:
                print(f"Error during recovery: {str(e2)}")
                
            # Try to continue with the test
            pass
        
        # Try to click close if we're back on the original window
        try:
            print("Checking if close button is present...")
            close_buttons = self.driver.find_elements(By.NAME, "close")
            if close_buttons:
                print("Close button found, attempting to click")
                close_buttons[0].click()
                print("Close button clicked")
                oncore_page.wait_between_actions()  # Wait after click
            else:
                print("No close button found")
        except Exception as e:
            print(f"Error trying to click close button: {str(e)}")
          # Save all performance data
        oncore_page.save_performance_data()

    def test_admin_performance(self):
        """Test the performance of Admin functions in OnCore"""
        # Use credentials stored in setUpClass
        username, password = self.__class__.username, self.__class__.password
        
        # Initialize the OnCore page object
        oncore_page = OncorePage(self.driver)
          # Navigate to the login page
        print("Loading login page...")
        oncore_page.navigate_to(self.base_url)
        oncore_page.measure_page_load("LoginPage")
        
        # Login with username and password, exit on failure
        try:
            oncore_page.login(username, password)  
        except Exception as e:
            print(f"Login failed: {str(e)}")
            print("Exiting test due to login failure.")
            import sys
            sys.exit(1)  # Exit with error status code
        
        # Navigate to home page
        print("Loading home page...")
        oncore_page.navigate_to("/smrs/SMRSHomePageServlet?hdn_function=WELCOME")
        oncore_page.wait_between_actions()  # Wait after navigation
        
        # Click RPE Console
        print("Opening RPE Console...")
        oncore_page.navigate_to(f"{self.base_url}/smrs/rpeAdministration/protocols/protocolDetails.do")
        oncore_page.wait_between_actions()  # Wait after navigation
        oncore_page.measure_page_load("AdminRPEConsole")
        
        # Click on oMTabOn element
        print("Clicking on Billing Grid tab...")
        oncore_page.navigate_to(f"{self.base_url}/smrs/rpeAdministration/protocolBillingGrid/pclBillingGrid.do")
        oncore_page.wait_between_actions()  # Wait after navigation
        oncore_page.measure_page_load("AdminBillingGrid")
        
        # Save all performance data
        oncore_page.save_performance_data("oncore_admin_performance.csv")


if __name__ == "__main__":
    unittest.main()