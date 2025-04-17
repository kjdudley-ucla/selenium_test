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


class OncorePerformanceTestGeneral(BaseTest):
    """Test case for OnCore performance testing using Page Object Model"""
    
    base_url = None
    username = None
    password = None
    protocol_no = None
    subject_mrn = None
    arm_name = None
    protocol_id = None
    @classmethod
    def setUpClass(cls):
        """Setup that runs once before all tests"""
        super().setUpClass()
        # Prompt for the number of iterations
        while True:
            try:
                cls.iterations = int(input("Enter the number of times to repeat each test: "))
                if cls.iterations > 0:
                    break
                else:
                    print("Please enter a positive number.")
            except ValueError:
                print("Please enter a valid number.")
        print(f"Tests will run {cls.iterations} time(s)")
        
        # Prompt for the testing environment URL
        cls.base_url = input("Enter the OnCore environment URL (e.g., https://crmsdev.mednet.ucla.edu): ")
        if not cls.base_url.startswith("http"):
            cls.base_url = "https://" + cls.base_url
        print(f"Using environment: {cls.base_url}")
        
        # Prompt for login credentials once
        cls.username = input("Enter your OnCore username: ")
        cls.password = getpass.getpass("Enter your OnCore password: ")
        print("Credentials stored for all test methods")
        
        # Prompt for protocol number
        cls.protocol_no = input("Enter the protocol number (e.g., 16-000265): ")
        print(f"Using protocol number: {cls.protocol_no}")

        # Prompt for protocol ID
        cls.protocol_id = input("Enter the protocol ID: ")
        print(f"Using protocol ID: {cls.protocol_id}")

        # Prompt for subject MRN
        cls.subject_mrn = input("Enter the test subject MRN: ")
        print(f"Using subject MRN: {cls.subject_mrn}")

        # Prompt for arm name
        cls.arm_name = input("Enter the arm name (e.g., BLD): ")
        print(f"Using arm: {cls.arm_name}")
        
        # Initialize current iteration
        cls.current_iteration = 1    
        
    def test_protocol_performance(self):
        """Test the performance of the protocol in OnCore"""
        # Use credentials stored in setUpClass
        username, password = self.__class__.username, self.__class__.password
        protocol_no = self.__class__.protocol_no
        subject_mrn = self.__class__.subject_mrn
        protocol_id = self.__class__.protocol_id
        current_iteration = self.__class__.current_iteration
        
        # Initialize the OnCore page object with the current iteration number
        oncore_page = OncorePage(self.driver, self.base_url, current_iteration)
        # Store oncore_page as an instance variable to ensure iteration is tracked
        self.oncore_page = oncore_page
        
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
            f"{self.base_url}/smrs/PRControlServlet?hdn_function=PROTOCOL_INQUIRY&hdn_function_type=INQUIRY&protocol_id={protocol_id}&protocol_no={protocol_no}&console=PC"
        )
        oncore_page.wait_between_actions()  # Wait after navigation
        oncore_page.measure_page_load(f"{protocol_no}Protocol")
          # Management Tab
        print("Loading Management tab...")
        # oncore_page.navigate_to(
        #     f"{self.base_url}/smrs/PRControlServlet?hdn_function=PROTOCOL_DETAILS&hdn_function_type=INQUIRY&protocol_no={protocol_no}&console=PC"
        # )
        oncore_page.execute_script("setActiveTab('PROTOCOL_DETAILS')")
        oncore_page.wait_between_actions()  # Wait after navigation
        oncore_page.measure_page_load(f"{protocol_no}Mgmt")
          # Staff Tab
        print("Loading Staff tab...")
        # oncore_page.navigate_to(
        #     f"{self.base_url}/smrs/PRControlServlet?hdn_function=PROTOCOL_STAFF&hdn_function_type=INQUIRY&protocol_no={protocol_no}&console=PC"
        # )
        oncore_page.execute_script("setActiveTab('PROTOCOL_STAFF')")
        oncore_page.wait_between_actions()  # Wait after navigation
        oncore_page.measure_page_load(f"{protocol_no}Staff")
          # Reviews Tab
        print("Loading Reviews tab...")
        # oncore_page.navigate_to(
        #     f"{self.base_url}/smrs/PRControlServlet?hdn_function=PROTOCOL_REVIEWS&hdn_function_type=INQUIRY&protocol_no={protocol_no}&console=PC"
        # )
        oncore_page.execute_script("setActiveTab('PROTOCOL_REVIEWS')")
        oncore_page.wait_between_actions()  # Wait after navigation
        oncore_page.measure_page_load(f"{protocol_no}Reviews")
          # Annotations Tab
        print("Loading Annotations tab...")
        # oncore_page.navigate_to(
        #     f"{self.base_url}/smrs/PRControlServlet?hdn_function=ANNOTATION_INQUIRY&hdn_function_type=INQUIRY&protocol_no={protocol_no}&console=PC"
        # )
        oncore_page.execute_script("setActiveTab('ANNOTATION_INQUIRY')")
        oncore_page.wait_between_actions()  # Wait after navigation
        oncore_page.measure_page_load(f"{protocol_no}Annotations")
          # CRA Console
        print("Loading CRA Console...")
        oncore_page.navigate_to(
            f"{self.base_url}/smrs/SMRSControlServlet?hdn_function=CRA_CONSOLE"
        )
        oncore_page.wait_between_actions()  # Wait after navigation
        oncore_page.measure_page_load(f"{protocol_no}CRA")

        # Subject Visit page measurement
        print("Loading Subject Visit...")
        # Take screenshot before looking for MRN
        print("Taking screenshot before MRN search...")
        self.driver.save_screenshot("before_mrn_search.png")
        
        # Print page source for debugging
        # print("Current page source:");
        # page_source = self.driver.page_source
        # print(page_source)
        
        print(f"Attempting to find subject MRN link for {subject_mrn}...")
        
        # Try multiple selector strategies
        try:
            # Strategy 1: Original exact match
            try:
                print("Trying exact match XPath...")
                mrn_link = WebDriverWait(oncore_page.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"//td[@value='{subject_mrn}']/a[text()='{subject_mrn}']"))
                )
                print("Found MRN link with exact match!")
            except TimeoutException:
                print("Exact match failed, trying alternative selectors...")
                
                # Strategy 2: Just look for the link text
                try:
                    print("Trying link text only...")
                    mrn_link = WebDriverWait(oncore_page.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, f"//a[contains(text(), '{subject_mrn}')]"))
                    )
                    print("Found MRN link by text only!")
                except TimeoutException:
                    print("Link text search failed, trying td approach...")
                    
                    # Strategy 3: Look for td with the value
                    try:
                        print("Trying td value approach...")
                        mrn_td = WebDriverWait(oncore_page.driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, f"//td[@value='{subject_mrn}']"))
                        )
                        # If td is found, look for anchor within it
                        mrn_link = mrn_td.find_element(By.TAG_NAME, "a")
                        print("Found MRN link through td!")
                    except TimeoutException:
                        print("All standard approaches failed. Trying broader search...")
                        
                        # Strategy 4: Super broad - any element containing the MRN
                        print("Trying broad text search...")
                        elements_with_mrn = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{subject_mrn}')]")
                        if elements_with_mrn:
                            print(f"Found {len(elements_with_mrn)} elements containing the MRN!")
                            print("Element details:")
                            for elem in elements_with_mrn:
                                print(f"Tag: {elem.tag_name}")
                                print(f"Text: {elem.text}")
                                print(f"HTML: {elem.get_attribute('outerHTML')}")
                            mrn_link = elements_with_mrn[0]
                        else:
                            raise Exception("Could not find MRN anywhere on the page")
            
            print("Found MRN link, attempting to click...")
            print(f"Link HTML: {mrn_link.get_attribute('outerHTML')}")
            mrn_link.click()
            print("Successfully clicked MRN link")
            oncore_page.wait_between_actions()  # Wait after clicking the link
            
        except Exception as e:
            print(f"Error finding/clicking MRN link: {str(e)}")
            self.driver.save_screenshot("mrn_search_failed.png")
            raise  # Re-raise the exception to fail the test
            
        oncore_page.measure_page_load(f"{protocol_no}SubjectVisit")
        
        # Calendar Tab
        print("Opening Calendar Tab...")
        oncore_page.execute_script("setActiveTab('SUBJECT_CALENDAR')")
        oncore_page.wait_between_actions()  # Wait after script execution
        oncore_page.measure_page_load(f"{protocol_no}Calendar")
        
        # On Study Tab
        print("Opening On Study Tab...")
        oncore_page.execute_script("setActiveTab('SUBJECT_ONSTUDY')")
        oncore_page.wait_between_actions()  # Wait after script execution
        oncore_page.measure_page_load(f"{protocol_no}OnStudy")
          # Return to CRA Console
        print("Returning to CRA Console...")
        oncore_page.navigate_to(
            f"{self.base_url}/smrs/SMRSControlServlet?hdn_function=CRA_CONSOLE"
        )
        oncore_page.wait_between_actions()  # Wait after navigation
        oncore_page.measure_page_load(f"{protocol_no}CRA2")
        
        # SAEs Tab via JavaScript
        print("Opening SAEs Tab...")
        oncore_page.execute_script("setTab('TOXICITIES', 'TOXICITIES')")
        oncore_page.wait_between_actions()  # Wait after script execution
        oncore_page.measure_page_load(f"{protocol_no}SAE")
        
        # Deviations Tab
        print("Opening Deviations Tab...")
        oncore_page.execute_script("setTab('DEVIATIONS', 'DEVIATIONS')")
        oncore_page.wait_between_actions()  # Wait after click
        oncore_page.measure_page_load(f"{protocol_no}Deviations")
          # Coverage Analysis
        print("Opening Coverage Analysis...")
        oncore_page.navigate_to(
            f"{self.base_url}/smrs/coverageAnalysisConsole/protocolSummary/details.do"
        )
        oncore_page.wait_between_actions()  # Wait after navigation
        oncore_page.measure_page_load(f"{protocol_no}CovA")
          # Procedures
        print("Opening Procedures...")
        oncore_page.navigate_to(f"{self.base_url}/smrs/coverageAnalysisConsole/procedures/all.do")
        oncore_page.wait_between_actions()  # Wait after navigation
        oncore_page.measure_page_load(f"{protocol_no}Proc")
        
        # Physical Exam
        print("Opening Physical Exam...")
        try:
            # Take a screenshot of current state
            self.driver.save_screenshot("before_physical_exam_search.png")
            print("Screenshot saved before searching for Physical Exam link")
            
            # Print current page source for debugging
            #print("Current page HTML:")
            #print(self.driver.page_source)
            
            # Try multiple strategies to find the Physical Exam link
            print("Looking for Physical Exam link with multiple strategies...")
            physical_exam_link = None
            
            strategies = [
                # Strategy 1: Original approach with th
                ("th with report-field-data class", "//th[@class='report-field-data']//a[contains(@href, 'javascript:toProcedureNotes') and (contains(normalize-space(.), 'Physical Exam') or contains(normalize-space(.), 'Physical Examination'))]"),
                
                # Strategy 2: Any link with Physical Exam text
                ("any Physical Exam link", "//a[contains(normalize-space(.), 'Physical Exam') or contains(normalize-space(.), 'Physical Examination')]"),
                
                # Strategy 3: Looking for the specific JavaScript function
                ("JavaScript function", "//a[contains(@href, 'javascript:toProcedureNotes')]"),
                
                # Strategy 4: Look for hidden input near Physical Exam
                ("hidden input approach", "//input[@type='hidden'][@name='ordered_procedure']/parent::*/a[contains(normalize-space(.), 'Physical Exam')]"),
                
                # Strategy 5: Case-insensitive search
                ("case-insensitive", "//a[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'physical exam')]"),
                
                # Strategy 6: Looking for any element containing Physical Exam
                ("broad search", "//*[contains(text(), 'Physical Exam') or contains(text(), 'Physical Examination')]"),
                
                # Strategy 7: Look for elements with specific width style
                ("style-based", "//th[@style='width: 200px']//a")
            ]
            
            for strategy_name, xpath in strategies:
                print(f"\nTrying strategy: {strategy_name}")
                try:
                    elements = self.driver.find_elements(By.XPATH, xpath)
                    if elements:
                        print(f"Found {len(elements)} potential matches with {strategy_name}")
                        for idx, elem in enumerate(elements):
                            try:
                                print(f"Element {idx + 1}:")
                                print(f"- Text content: {elem.text}")
                                print(f"- HTML: {elem.get_attribute('outerHTML')}")
                                print(f"- href: {elem.get_attribute('href')}")
                                print(f"- onclick: {elem.get_attribute('onclick')}")
                                print(f"- Is displayed: {elem.is_displayed()}")
                                print(f"- Is enabled: {elem.is_enabled()}")
                                
                                # If this is our first found element and we haven't set physical_exam_link yet
                                if physical_exam_link is None:
                                    # Try to ensure it's clickable
                                    wait = WebDriverWait(self.driver, 10)
                                    physical_exam_link = wait.until(EC.element_to_be_clickable((By.XPATH, f"({xpath})[{idx + 1}]")))
                                    print(f"Selected element {idx + 1} as our target")
                                    break
                            except Exception as e:
                                print(f"Error examining element {idx + 1}: {str(e)}")
                                continue
                    else:
                        print(f"No elements found with {strategy_name}")
                except Exception as e:
                    print(f"Error with strategy {strategy_name}: {str(e)}")
                    continue
                
                if physical_exam_link is not None:
                    print(f"Successfully found clickable element using strategy: {strategy_name}")
                    break
            
            if physical_exam_link is None:
                print("No strategies succeeded in finding the Physical Exam link")
                print("Taking screenshot of failure state...")
                self.driver.save_screenshot("physical_exam_all_strategies_failed.png")
                raise Exception("Could not find Physical Exam link with any strategy")

            # Try to click the element
            try:
                print("Attempting to click the found element...")
                physical_exam_link.click()
                print("Successfully clicked the Physical Exam link")
            except Exception as e:
                print(f"Error clicking element: {str(e)}")
                print("Trying JavaScript click as fallback...")
                self.driver.execute_script("arguments[0].click();", physical_exam_link)
                print("Executed JavaScript click")
            
            oncore_page.wait_between_actions()  # Wait after click
            oncore_page.measure_page_load(f"{protocol_no}PhysEx")
            
        except Exception as e:
            print(f"Error handling Physical Exam link: {str(e)}")
            self.driver.save_screenshot("physical_exam_error.png")
            raise  # Re-raise the exception to fail the test

          # Billing Grid
        print("Opening Billing Grid...")
        oncore_page.navigate_to(f"{self.base_url}/smrs/coverageAnalysisConsole/billingGrid/display.do")
        oncore_page.wait_between_actions()  # Wait after navigation
        oncore_page.measure_page_load(f"{protocol_no}BG")
          # Financials Console
        print("Opening Financials Console...")
        oncore_page.navigate_to(
            f"{self.base_url}/smrs/SMRSControlServlet?hdn_function=PROTOCOL_BUDGET"
        )
        oncore_page.wait_between_actions()  # Wait after navigation
        oncore_page.measure_page_load(f"{protocol_no}Financials")
        
        # Subject Related Tab
        print("Opening Subject Related Tab...")
        # oncore_page.click_element((By.CSS_SELECTOR, "tr:nth-child(5) > .oMTab"))
        oncore_page.execute_script("setActiveTab('PROCEDURE', 'Procedure/Lab')")
        oncore_page.wait_between_actions()  # Wait after click
        oncore_page.measure_page_load(f"{protocol_no}SubRel")
        
        # Physical Exam Procedure
        print("Opening Physical Exam Procedure...")
        # link = WebDriverWait(oncore_page.driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'javascript:toProcedureDetails') and (contains(text(), 'Physical Exam') or contains(text(), 'Physical Examination'))]"))
        # )
        try:
            # Take a screenshot of current state
            self.driver.save_screenshot("before_physical_exam_search.png")
            print("Screenshot saved before searching for Physical Exam link")
            
            # Print current page source for debugging
            #print("Current page HTML:")
            #print(self.driver.page_source)
            
            # Try multiple strategies to find the Physical Exam link
            print("Looking for Physical Exam link with multiple strategies...")
            physical_exam_link = None
            
            strategies = [
                # Strategy 1: Original approach with th
                ("th with report-field-data class", "//th[@class='report-field-data']//a[contains(@href, 'javascript:toProcedureDetails') and (contains(normalize-space(.), 'Physical Exam') or contains(normalize-space(.), 'Physical Examination'))]"),
                
                # Strategy 2: Any link with Physical Exam text
                ("any Physical Exam link", "//a[contains(normalize-space(.), 'Physical Exam') or contains(normalize-space(.), 'Physical Examination')]"),
                
                # Strategy 3: Looking for the specific JavaScript function
                ("JavaScript function", "//a[contains(@href, 'javascript:toProcedureDetails')]"),
                
                # Strategy 4: Look for hidden input near Physical Exam
                ("hidden input approach", "//input[@type='hidden'][@name='ordered_procedure']/parent::*/a[contains(normalize-space(.), 'Physical Exam')]"),
                
                # Strategy 5: Case-insensitive search
                ("case-insensitive", "//a[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'physical exam')]"),
                
                # Strategy 6: Looking for any element containing Physical Exam
                ("broad search", "//*[contains(text(), 'Physical Exam') or contains(text(), 'Physical Examination')]"),
                
                # Strategy 7: Look for elements with specific width style
                ("style-based", "//th[@style='width: 200px']//a")
            ]
            
            for strategy_name, xpath in strategies:
                print(f"\nTrying strategy: {strategy_name}")
                try:
                    elements = self.driver.find_elements(By.XPATH, xpath)
                    if elements:
                        print(f"Found {len(elements)} potential matches with {strategy_name}")
                        for idx, elem in enumerate(elements):
                            try:
                                print(f"Element {idx + 1}:")
                                print(f"- Text content: {elem.text}")
                                print(f"- HTML: {elem.get_attribute('outerHTML')}")
                                print(f"- href: {elem.get_attribute('href')}")
                                print(f"- onclick: {elem.get_attribute('onclick')}")
                                print(f"- Is displayed: {elem.is_displayed()}")
                                print(f"- Is enabled: {elem.is_enabled()}")
                                
                                # If this is our first found element and we haven't set physical_exam_link yet
                                if physical_exam_link is None:
                                    # Try to ensure it's clickable
                                    wait = WebDriverWait(self.driver, 10)
                                    physical_exam_link = wait.until(EC.element_to_be_clickable((By.XPATH, f"({xpath})[{idx + 1}]")))
                                    print(f"Selected element {idx + 1} as our target")
                                    break
                            except Exception as e:
                                print(f"Error examining element {idx + 1}: {str(e)}")
                                continue
                    else:
                        print(f"No elements found with {strategy_name}")
                except Exception as e:
                    print(f"Error with strategy {strategy_name}: {str(e)}")
                    continue
                
                if physical_exam_link is not None:
                    print(f"Successfully found clickable element using strategy: {strategy_name}")
                    break
            
            if physical_exam_link is None:
                print("No strategies succeeded in finding the Physical Exam link")
                print("Taking screenshot of failure state...")
                self.driver.save_screenshot("physical_exam_all_strategies_failed.png")
                raise Exception("Could not find Physical Exam link with any strategy")

            # Try to click the element
            try:
                print("Attempting to click the found element...")
                physical_exam_link.click()
                print("Successfully clicked the Physical Exam link")
            except Exception as e:
                print(f"Error clicking element: {str(e)}")
                print("Trying JavaScript click as fallback...")
                self.driver.execute_script("arguments[0].click();", physical_exam_link)
                print("Executed JavaScript click")
            
            oncore_page.wait_between_actions()  # Wait after click
            oncore_page.wait_between_actions()  # Wait after click
            oncore_page.measure_page_load(f"{protocol_no}PhysEx2")
        except Exception as e:
            print(f"Error handling Physical Exam link: {str(e)}")
            self.driver.save_screenshot("physical_exam_error.png")
            raise  # Re-raise the exception to fail the test
        
        # Close
        print("Closing dialog...")
        oncore_page.click_element(oncore_page.CLOSE_BUTTON)
        oncore_page.wait_between_actions()  # Wait after click
        
        # Invoicable Items Tab
        print("Opening Invoicable Items Tab...")
        oncore_page.execute_script("toInvoicableItems()")
        oncore_page.wait_between_actions()  # Wait after click
        oncore_page.measure_page_load(f"{protocol_no}Inv")
          # Specifications
        print("Opening Specifications...")
        oncore_page.navigate_to(
            f"{self.base_url}/smrs/SMRSControlServlet?hdn_function=STUDY_SETUP"
        )
        oncore_page.wait_between_actions()  # Wait after navigation
        oncore_page.measure_page_load(f"{protocol_no}Spec")
        
        # Select Arm using user-provided arm name
        print(f"Selecting arm: {self.__class__.arm_name}...")
        arm_dropdown = oncore_page.driver.find_element(By.ID, "arm_selector")
        select = Select(arm_dropdown)
        select.select_by_visible_text(self.__class__.arm_name)  # Select the user-specified arm
        oncore_page.wait_between_actions()  # Wait after selection
        oncore_page.measure_page_load(f"{protocol_no}SelectArm")
        
        # Open Physical Exam procedure from specifications
        print("Opening Physical Exam procedure...")
        try:
            # Take a screenshot of current state
            self.driver.save_screenshot("before_physical_exam_search.png")
            print("Screenshot saved before searching for Physical Exam link")
            
            # Print current page source for debugging
            #print("Current page HTML:")
            #print(self.driver.page_source)
            
            # Try multiple strategies to find the Physical Exam link
            print("Looking for Physical Exam link with multiple strategies...")
            physical_exam_link = None
            
            strategies = [
                # Strategy 1: Original approach with th
                ("th with report-field-data class", "//th[@class='report-field-data']//a[contains(@href, 'javascript:toProcedureDetails') and (contains(normalize-space(.), 'Physical Exam') or contains(normalize-space(.), 'Physical Examination'))]"),
                
                # Strategy 2: Any link with Physical Exam text
                ("any Physical Exam link", "//a[contains(normalize-space(.), 'Physical Exam') or contains(normalize-space(.), 'Physical Examination')]"),
                
                # Strategy 3: Looking for the specific JavaScript function
                ("JavaScript function", "//a[contains(@href, 'javascript:toProcedureDetails')]"),
                
                # Strategy 4: Look for hidden input near Physical Exam
                ("hidden input approach", "//input[@type='hidden'][@name='ordered_procedure']/parent::*/a[contains(normalize-space(.), 'Physical Exam')]"),
                
                # Strategy 5: Case-insensitive search
                ("case-insensitive", "//a[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'physical exam')]"),
                
                # Strategy 6: Looking for any element containing Physical Exam
                ("broad search", "//*[contains(text(), 'Physical Exam') or contains(text(), 'Physical Examination')]"),
                
                # Strategy 7: Look for elements with specific width style
                ("style-based", "//th[@style='width: 200px']//a")
            ]
            
            for strategy_name, xpath in strategies:
                print(f"\nTrying strategy: {strategy_name}")
                try:
                    elements = self.driver.find_elements(By.XPATH, xpath)
                    if elements:
                        print(f"Found {len(elements)} potential matches with {strategy_name}")
                        for idx, elem in enumerate(elements):
                            try:
                                print(f"Element {idx + 1}:")
                                print(f"- Text content: {elem.text}")
                                print(f"- HTML: {elem.get_attribute('outerHTML')}")
                                print(f"- href: {elem.get_attribute('href')}")
                                print(f"- onclick: {elem.get_attribute('onclick')}")
                                print(f"- Is displayed: {elem.is_displayed()}")
                                print(f"- Is enabled: {elem.is_enabled()}")
                                
                                # If this is our first found element and we haven't set physical_exam_link yet
                                if physical_exam_link is None:
                                    # Try to ensure it's clickable
                                    wait = WebDriverWait(self.driver, 10)
                                    physical_exam_link = wait.until(EC.element_to_be_clickable((By.XPATH, f"({xpath})[{idx + 1}]")))
                                    print(f"Selected element {idx + 1} as our target")
                                    break
                            except Exception as e:
                                print(f"Error examining element {idx + 1}: {str(e)}")
                                continue
                    else:
                        print(f"No elements found with {strategy_name}")
                except Exception as e:
                    print(f"Error with strategy {strategy_name}: {str(e)}")
                    continue
                
                if physical_exam_link is not None:
                    print(f"Successfully found clickable element using strategy: {strategy_name}")
                    break
            
            if physical_exam_link is None:
                print("No strategies succeeded in finding the Physical Exam link")
                print("Taking screenshot of failure state...")
                self.driver.save_screenshot("physical_exam_all_strategies_failed.png")
                raise Exception("Could not find Physical Exam link with any strategy")

            # Try to click the element
            try:
                print("Attempting to click the found element...")
                physical_exam_link.click()
                print("Successfully clicked the Physical Exam link")
            except Exception as e:
                print(f"Error clicking element: {str(e)}")
                print("Trying JavaScript click as fallback...")
                self.driver.execute_script("arguments[0].click();", physical_exam_link)
                print("Executed JavaScript click")
            
            oncore_page.wait_between_actions()  # Wait after click
            oncore_page.measure_page_load(f"{protocol_no}PhysEx3")
        except Exception as e:
            print(f"Error handling Physical Exam link: {str(e)}")
            self.driver.save_screenshot("physical_exam_error.png")
            raise  # Re-raise the exception to fail the test
        
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
            # Look for a link with text "Visits" and click it if found
            try:
                visits_link = WebDriverWait(oncore_page.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//a[text()='Visits'][1]"))
                )
                print("Found 'Visits' link, clicking it...")
                visits_link.click()
                oncore_page.wait_between_actions()  # Wait after clicking
            except TimeoutException:
                print("No 'Visits' link found on the page, continuing with test...")
                self.driver.save_screenshot("no_visits_link.png")
            
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
                    oncore_page.measure_page_load(f"{protocol_no}Visits")
                    
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
                                oncore_page.measure_page_load(f"{protocol_no}Submit")
                            except TimeoutException:
                                print("TimeoutException occurred when trying to click submit button")
                                # Try alternative approach - click the first submit button directly
                                print("Trying alternative approach - direct click")
                                submit_buttons[0].click()
                                print("Submit button clicked directly")
                                oncore_page.wait_between_actions()  # Wait after click
                                oncore_page.measure_page_load(f"{protocol_no}Submit")
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
          # Initialize the OnCore page object with the current iteration
        oncore_page = OncorePage(self.driver, self.base_url, self.__class__.current_iteration)
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
    # If running this module as a script, bypass unittest.main() and handle iterations manually
    test_class = OncorePerformanceTestGeneral
    test_class.setUpClass()
    try:
        for iteration in range(1, test_class.iterations + 1):
            print(f"\n\n======= Starting Iteration {iteration} of {test_class.iterations} =======\n")
            
            # Create a test instance
            test_instance = test_class("test_protocol_performance")
            test_class.current_iteration = iteration
            
            # Set up the test environment
            test_instance.setUp()
            
            try:
                # Create the OnCore page with the current iteration number
                test_instance.oncore_page = OncorePage(test_instance.driver, test_instance.base_url, iteration)
                
                # Run the test
                test_instance.test_protocol_performance()
                print(f"\n✓ Iteration {iteration} completed successfully")
            except Exception as e:
                print(f"\n✗ Iteration {iteration} failed: {str(e)}")
            finally:
                # Clean up after the test
                test_instance.tearDown()
                
            # Add a separator between iterations
            print(f"\n======= End of Iteration {iteration} =======\n")
            
            # Optionally add a pause between iterations
            if iteration < test_class.iterations:
                print(f"Waiting 10 seconds before starting the next iteration...")
                time.sleep(10)
                  # Also run the admin performance test for each iteration
        for iteration in range(1, test_class.iterations + 1):
            print(f"\n\n======= Running Admin Performance Test (Iteration {iteration}) =======\n")
            admin_test_instance = test_class("test_admin_performance")
            test_class.current_iteration = iteration
            admin_test_instance.setUp()
            
            try:
                # Create the OnCore page with the current iteration number
                admin_test_instance.oncore_page = OncorePage(admin_test_instance.driver, admin_test_instance.base_url, iteration)
                
                # Run the admin test
                admin_test_instance.test_admin_performance()
                print(f"\n✓ Admin test iteration {iteration} completed successfully")
            except Exception as e:
                print(f"\n✗ Admin test iteration {iteration} failed: {str(e)}")
            finally:
                # Clean up after the test
                admin_test_instance.tearDown()
                
            # Add a pause between iterations if not the last one
            if iteration < test_class.iterations:
                print(f"Waiting 5 seconds before next admin test iteration...")
                time.sleep(5)
    except KeyboardInterrupt:
        print("\nTest execution interrupted by user.")
    except Exception as e:
        print(f"\nAn error occurred during test execution: {str(e)}")
    finally:
        print("\nTest execution complete.")