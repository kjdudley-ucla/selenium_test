# Selenium Test Framework with Python for OnCore Performance Testing

A comprehensive test automation framework using Python and Selenium WebDriver to automate browser testing and performance measurement of OnCore applications.

## Project Structure

- `base_test.py` - Base test class with common setup and teardown routines
- `oncore_performance_test_general.py` - Enhanced OnCore performance test with user prompts
- `selenium_utils.py` - Utility functions for Selenium interactions
- `page_objects/` - Directory containing Page Object Model classes
  - `oncore_page.py` - Page object for OnCore application pages

## Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `.\venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running OnCore Performance Tests

### Running the General Performance Test

To run the OnCore performance test with user prompts:
```
python oncore_performance_test_general.py
```

The test will prompt for:
- OnCore environment URL
- Username
- Password
- Protocol number
- Protocol ID
- Subject MRN
- Arm name

### Test Features

The performance test includes measurements for:
- Login page load time
- Protocol Information page load time
- Management tab load time
- Staff tab load time
- Reviews tab load time
- Annotations tab load time
- CRA Console load time
- Subject Visit page load time
- Calendar tab load time
- On Study tab load time
- SAEs tab load time
- Deviations tab load time
- Coverage Analysis load time
- Procedures load time
- Physical Exam procedure load time
- Billing Grid load time
- Financials Console load time
- Specifications load time

### Test Output

The test generates:
- Performance metrics in CSV format
- Screenshots for debugging purposes
- Detailed console logs of test progression

## Framework Features

- **Page Object Model**: Separation of page structure from test logic
- **Base Test Class**: Common setup/teardown routines
- **Performance Measurement**: Automatic timing of page loads and operations
- **Screenshots**: Automatic capture of screenshots for debugging
- **Webdriver Management**: Automatic download and management of Chrome WebDriver
- **Error Handling**: Robust error handling with screenshots on failure
- **User Input Handling**: Interactive prompts for test configuration

## Debugging Features

The framework includes extensive debugging capabilities:
- Screenshots at critical points
- Detailed console logging
- Multiple strategies for element location
- Error state capture
- Window handling debugging

## Notes

- Screenshots are saved in the project root directory
- Performance data is saved in CSV format
- The framework handles both single-window and multi-window operations
- Includes special handling for OnCore-specific elements and JavaScript interactions
