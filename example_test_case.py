from base_test import BaseTest
from page_objects.example_page import ExamplePage
import unittest


class ExampleDomainTest(BaseTest):
    """Test case for Example.com website using Page Object Model"""
    
    def test_example_page_content(self):
        """Test the content of example.com"""
        # Initialize the Example page object
        example_page = ExamplePage(self.driver)
        
        # Navigate and wait for page to load
        example_page.navigate().wait_for_page_load()
        
        # Take a screenshot
        example_page.take_screenshot("example_domain_test.png")
        
        # Verify page elements and content
        header_text = example_page.get_header_text()
        self.assertEqual("Example Domain", header_text, 
                         "Header text should be 'Example Domain'")
        
        paragraph_text = example_page.get_paragraph_text()
        self.assertIn("illustrative examples", paragraph_text, 
                     "Paragraph should contain 'illustrative examples'")
        
        # Check if more info link exists
        has_more_info = example_page.has_more_info_link()
        self.assertTrue(has_more_info, "More information link should be present")
        
        # Verify text in page source
        page_source = example_page.get_page_source()
        self.assertIn("Example Domain", page_source, 
                     "Page source should contain 'Example Domain'")


if __name__ == "__main__":
    unittest.main()