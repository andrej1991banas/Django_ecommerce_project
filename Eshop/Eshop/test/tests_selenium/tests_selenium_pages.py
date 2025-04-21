import os
import django

# Explicitly set the DJANGO_SETTINGS_MODULE variable at runtime if not set
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eshop.settings")
django.setup()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By
import time




class MyTests(LiveServerTestCase):
    def setUp(self):
        service = Service(r"C:\Users\limit\Selenium_drivers\chromedriver.exe")  # Be sure to include 'chromedriver.exe'

        # Optional: Add Chrome options if needed
        options = Options()
        options.add_argument("--headless") #ptional with no vizualization of the testing processes
        options.add_argument('--start-maximized')  # Open browser in maximized mode
        options.add_argument('--disable-extensions')  # Disable extensions for faster loading

        # Instantiate the WebDriver with the Service
        self.driver = webdriver.Chrome(service=service, options=options)



    def test_homepage(self):
        # Access the test server's homepage
        driver= self.driver

        driver.get(self.live_server_url)
        time.sleep(2)
        driver.maximize_window()
        driver.get_screenshot_as_file('eshop\\test\\tests_screenshots\\selenium_test_page_pics\\screenshot_homepage.png')

        # Example: Verify an element's text
        title = self.driver.title
        els = self.driver.find_elements(By.TAG_NAME, "p")

        self.assertEqual(title, "Django Ecomm")  # Replace "Django Ecomm" with the actual title
        self.assertIn("© 2025 Fly Fishing Shop. All rights reserved.", els[-1].text)
        print("Homepage url successfully loaded! ")


    def test_about(self):
        # Access the test server's homepage
        driver = self.driver

        driver.get(self.live_server_url)
        time.sleep(2)

        # Find and follow link to about page
        about_link = self.driver.find_element(By.LINK_TEXT, "About |")
        about_link.click()
        self.assertEqual(driver.current_url, self.live_server_url +"/about")

        #wait till the page is loaded
        time.sleep(5)
        driver.get_screenshot_as_file('eshop\\test\\tests_screenshots\\selenium_test_page_pics\\screenshot_about.png')

        # Example: Verify an element's text
        header = self.driver.find_element(By.TAG_NAME, "h1").text
        self.assertEqual(header, "About Us ...")  # Replace "Django Ecomm" with the actual title
        print("About url successfully loaded! ")


    def test_register_page(self):
        # Access the test server's homepage
        driver = self.driver

        driver.get(self.live_server_url)
        time.sleep(2)

        # Find and follow link to about page
        register_link = self.driver.find_element(By.LINK_TEXT, "Register |")
        register_link.click()
        time.sleep(5)# wait till the page is loaded
        self.assertEqual(driver.current_url, self.live_server_url +"/register")

        driver.get_screenshot_as_file('eshop\\test\\tests_screenshots\\selenium_test_page_pics\\screenshot_register.png')

        # Example: Verify an element's text
        header = self.driver.find_element(By.TAG_NAME, "h1").text
        self.assertEqual(header, "Create Your Account")  # Replace "Django Ecomm" with the actual title
        print("Register url successfully loaded! ")


    def test_log_in_page(self):
          #Access the test server's homepage
        driver = self.driver

        driver.get(self.live_server_url)
        time.sleep(2)

        # Find and follow link to about page
        register_link = self.driver.find_element(By.LINK_TEXT, "Sign In |")
        register_link.click()
        time.sleep(5)# wait till the page is loaded

        driver.get_screenshot_as_file('eshop\\test\\tests_screenshots\\selenium_test_page_pics\\screenshot_login.png')
        self.assertEqual(driver.current_url, self.live_server_url +"/login")
        print("Login url successfully loaded! ")


    def test_shop_search_dropdown(self):
        # Access the test server's homepage
        driver = self.driver

        driver.get(self.live_server_url)
        time.sleep(2)

        # Find and follow link to about page
        dropdown_toggle = driver.find_element(By.ID, "navbarDropdown")
        dropdown_toggle.click()
        time.sleep(1)  # wait till the page is loaded
          #iterate through the dropdown menu and return page, we will get not found 404 error page as we do not have any categries, will test visualization of the pages in different test case
        dropdown_menu = driver.find_element(By.CSS_SELECTOR, "ul.dropdown-menu > li:nth-child(1) > a.dropdown-item")
        dropdown_menu.click()
        time.sleep(2)

        driver.get_screenshot_as_file('eshop\\test\\tests_screenshots\\selenium_test_page_pics\\screenshot_all_products.png')
        self.assertEqual(driver.current_url, self.live_server_url + "/show-products")
        print("Search all products url successfully loaded! ")


        driver.back()  # Return to the previous page
        time.sleep(2)

        dropdown_toggle = driver.find_element(By.ID, "navbarDropdown")
        dropdown_toggle.click()
        time.sleep(1)  # wait till the page is loaded

        dropdown_menu = driver.find_element(By.CSS_SELECTOR, "ul.dropdown-menu > li:nth-child(3) > a.dropdown-item")
        dropdown_menu.click()
        time.sleep(5)

        driver.get_screenshot_as_file('eshop\\test\\tests_screenshots\\selenium_test_page_pics\\screenshot_rods_category.png')
        self.assertEqual(driver.current_url, self.live_server_url + "/category/1/")

        driver.back()  # Return to the previous page
        time.sleep(2)

        dropdown_toggle = driver.find_element(By.ID, "navbarDropdown")
        dropdown_toggle.click()
        time.sleep(1)  # wait till the page is loaded

        dropdown_menu = driver.find_element(By.CSS_SELECTOR, "ul.dropdown-menu > li:nth-child(4) > a.dropdown-item")
        dropdown_menu.click()
        time.sleep(2)

        #we will get 404 page not found error as we do not have any created category neither product added to the category
        driver.get_screenshot_as_file(
            'eshop\\test\\tests_screenshots\\selenium_test_page_pics\\screenshot_rods_category.png')
        self.assertEqual(driver.current_url, self.live_server_url + "/category/2/")
        print("Search category url successfully loaded! ")


    def test_search_link_with_input(self):
        # Access the test server's homepage
        driver = self.driver

        driver.get(self.live_server_url)
        time.sleep(2)

        # Locate the search input field and type a value
        search_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search ...']")
        search_input.send_keys("Test Search")

        # Locate and click the search button
        search_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        search_button.click()
        time.sleep(5)
        driver.get_screenshot_as_file('eshop\\test\\tests_screenshots\\selenium_test_page_pics\\screenshot_search.png')
        self.assertEqual(driver.current_url, self.live_server_url + "/search")
        print("Search url successfully loaded! ")


    def test_cart_summary(self):
         #Access the test server's homepage
        driver = self.driver

        driver.get(self.live_server_url)
        time.sleep(2)
        cart = driver.find_element(By.CLASS_NAME, "cart_link")
        cart.click()
        time.sleep(5)
        driver.get_screenshot_as_file('eshop\\test\\tests_screenshots\\selenium_test_page_pics\\screenshot_cart_summary.png')
        self.assertEqual(driver.current_url, self.live_server_url + "/cart")
        print ("Cart url successfully loaded! ")

    def tearDown(self):
        # Quit the browser after the test is complete
        self.driver.quit()