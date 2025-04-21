import os
import django

# Explicitly set the DJANGO_SETTINGS_MODULE variable at runtime if not set
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eshop.settings")
django.setup()


from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from django.test import LiveServerTestCase
from selenium.webdriver.support.ui import Select, WebDriverWait
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

    def test_crud_with_user_member_process(self):
        # Access the test server's homepage
        driver = self.driver

        driver.get(self.live_server_url+"/register") #load register page
        time.sleep(2)

        #find and indentify fields from the register form
        username_field = driver.find_element(By.NAME, "username")
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password1")
        password_field2 = driver.find_element(By.NAME, "password2")
        first_name_field = driver.find_element(By.NAME, "first_name")
        last_name_field = driver.find_element(By.NAME, "last_name")
        phone_field = driver.find_element(By.NAME, "phone_number")

        register_button = driver.find_element(By.XPATH, "//input[@value='Register']")

        #creating and input for testing credentials
        username_field.send_keys("testuser")
        email_field.send_keys("testuser@example.com")
        password_field.send_keys("Speyya1991????")
        password_field2.send_keys("Speyya1991????")
        first_name_field.send_keys("andrejtest")
        last_name_field.send_keys("banastest")
        phone_field.send_keys("123456789")
        driver.get_screenshot_as_file('eshop\\test\\tests_screenshots\\selenium_crud_member_pics\\screenshot_register_with_input.png')
        print("Test case used credentials")
        # wait for ipnuted data and redirecting to login page
        register_button.click()

        time.sleep(5)
        driver.get_screenshot_as_file('eshop\\test\\tests_screenshots\\selenium_crud_member_pics\\screenshot_registered_user.png')
        self.assertEqual(driver.current_url, self.live_server_url +"/login") #assert redirect to the login page
        print("User created!")

        """ Test log in for user"""

        #find fields from the log in form
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")

        login_button = driver.find_element(By.XPATH, "//input[@value='Login']")

        # logging in and input for testing credentials
        username_field.send_keys("testuser")
        password_field.send_keys("Speyya1991????")
        driver.get_screenshot_as_file(
            'eshop\\test\\tests_screenshots\\selenium_crud_member_pics\\screenshot_login_data_user.png')

        login_button.click()
        time.sleep(5)

        driver.get_screenshot_as_file('eshop\\test\\tests_screenshots\\selenium_crud_member_pics\\screenshot_logged_in_user.png')
        self.assertEqual(driver.current_url, self.live_server_url + "/dashboard") #assert redirect to the dashboard page
        print("User logged in!")
        print("Current url:", driver.current_url)

        #after redirecting to dashboard lets update the member data
        update_button = driver.find_element(By.LINK_TEXT, "Update Profile")
        update_button.click()
        time.sleep(5)
        print("Redirected from dashboard to update page")

        """ Test only update the member info not shipping address and getting only member update message"""

        # find fields from the update user form
        city_field = driver.find_element(By.NAME, "city")


        # logging in and input for testing credentials
        city_field.send_keys("Lokca")

        time.sleep(2)

        update_button_user = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "update-profile"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", update_button_user)
        time.sleep(1)  # Ensure the scroll action is completed
        update_button_user.click()


        # Wait for the success message to appear (e.g., a div with class "alert-success")
        success_message = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
        )
        # verify success message and updated data in profile info
        driver.get_screenshot_as_file(
            'eshop\\test\\tests_screenshots\\selenium_crud_member_pics\\screenshot_update_only_member_data.png')

        self.assertEqual(driver.current_url, self.live_server_url + "/update") #assert stay on  the update page
        # Verify the success message text
        self.assertIn("Your account has been updated!", success_message.text)
        print("Updated member info!")


        """ Test for Shipping address update and success update message """

        #find the fields for updating the shipping address form
        shipping_first_name_field = driver.find_element(By.NAME, "shipping_first_name")
        shipping_last_name_field = driver.find_element(By.NAME, "shipping_last_name")

        # update Shipping address form and model
        shipping_first_name_field.send_keys("AndrejTest")
        shipping_last_name_field.send_keys("BanasTest")
        time.sleep(2)

        update_button_shipping = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "update-profile"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", update_button_shipping)
        time.sleep(1)  # Ensure the scroll action is completed
        update_button_shipping.click()

        # Wait for the success message to appear (e.g., a div with class "alert-success")
        success_message = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
        )

        self.assertEqual(driver.current_url, self.live_server_url + "/update")  # assert stay on  the update page
        # Verify the success message text
        self.assertIn("Your account has been updated!", success_message.text)

        # verify success message and updated data in profile info
        driver.get_screenshot_as_file(
            'eshop\\test\\tests_screenshots\\selenium_crud_member_pics\\screenshot_update_only_shipping_data.png')
        print("Updated member shipping info!")

        """ Test for member info update and  Shipping address update and success update message for both changes"""

        # find fields from the update user form
        city_field = driver.find_element(By.NAME, "city")
        gender_dropdown = driver.find_element(By.NAME, "gender")
        country_field = driver.find_element(By.NAME, "country")

        #find the fields for updating the shipping address form
        shipping_first_name_field = driver.find_element(By.NAME, "shipping_first_name")
        shipping_last_name_field = driver.find_element(By.NAME, "shipping_last_name")
        shipping_email_field = driver.find_element(By.NAME, "shipping_email")
        shipping_address1_field = driver.find_element(By.NAME, "shipping_address1")
        shipping_city_field = driver.find_element(By.NAME, "shipping_city")
        shipping_zipcode_field = driver.find_element(By.NAME, "shipping_zipcode")
        shipping_country_field = driver.find_element(By.NAME, "shipping_country")

        # logging in and input for testing credentials
        city_field.send_keys("Bratislava")
        # # Initialize the Select class
        select_gender = Select(gender_dropdown)
        select_gender.select_by_visible_text("Male")
        country_field.send_keys("UK")

        # update Shipping address form and model
        shipping_first_name_field.send_keys("Testupdate")
        shipping_last_name_field.send_keys("TestLastName")
        shipping_email_field.send_keys("andrej@gmail.com")
        shipping_address1_field.send_keys("breyova523")
        shipping_city_field.send_keys("Bratislava")
        shipping_zipcode_field.send_keys("12345")
        shipping_country_field.send_keys("Slovakia")
        time.sleep(2)

        update_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "update-profile"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", update_button)
        time.sleep(1)  # Ensure the scroll action is completed
        update_button.click()

        # Wait for the success message to appear (e.g., a div with class "alert-success")
        success_message = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
        )

        self.assertEqual(driver.current_url, self.live_server_url + "/update")  # assert stay on  the update page
        # Verify the success message text
        self.assertIn("Your account and shipping address have been updated!", success_message.text)

        # verify success message and updated data in profile info
        driver.get_screenshot_as_file(
            'eshop\\test\\tests_screenshots\\selenium_crud_member_pics\\screenshot_update_all_data.png')
        print("Updated member personal and shipping info!")


        """ Test update password case"""

        driver.get(self.live_server_url + "/dashboard")  # load register page

        # Wait explicitly for the "Update Password" button to be clickable
        update_password = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Update Password"))
        )
        update_password.click()  # Proceed with clicking the button
        print("Current url:", driver.current_url)


        #find fields for input the new password
        new_password1_field = driver.find_element(By.NAME, "new_password1")
        new_password2_field = driver.find_element(By.NAME, "new_password2")
        change_button = driver.find_element(By.XPATH, "//input[@value='Change Password']")

        #input new data into the form and change password
        new_password1_field.send_keys("Spezza1991?")
        new_password2_field.send_keys("Spezza1991?")
        change_button.click()


        # Wait for the login page to load
        WebDriverWait(driver, 10).until(
            EC.url_to_be(self.live_server_url + "/login")
        )

        # Re-locate the success message
        success_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
        )

        # Assert the success message and URL
        self.assertIn("Your password has been updated! Please log in again", success_message.text)
        self.assertEqual(driver.current_url, self.live_server_url + "/login")

        driver.get_screenshot_as_file(
            'eshop\\test\\tests_screenshots\\selenium_crud_member_pics\\screenshot_update_password.png')
        print("Password updated!")

        """ Test delete user case """

        # find fields from the log in form
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        login_button2 = driver.find_element(By.XPATH, "//input[@value='Login']")

        # logging in and input for testing credentials
        username_field.send_keys("testuser")
        password_field.send_keys("Spezza1991?")
        login_button2.click()

        # Wait for the dashboard to load
        WebDriverWait(driver, 10).until(
            EC.url_to_be(self.live_server_url + "/dashboard")
        )

        # Debug: Print current URL and take a screenshot
        print("Current URL after login:", driver.current_url)
        assert driver.current_url == f"{self.live_server_url}/dashboard"
        # Wait for the "Delete Account" button to be clickable
        delete_account_button = WebDriverWait(driver, 25).until(
            EC.element_to_be_clickable((By.ID, "delete-account")))
        delete_account_button.click()

        modal_title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "deleteModalLabel"))  # Modal title ID
        )

        # Wait for and click the "Delete" button inside the modal
        delete_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@id='deleteModal']//a[@class='btn btn-danger']"))
        )
        delete_button.click()

        # Wait for the index page to load
        WebDriverWait(driver, 50).until(
            EC.url_to_be(self.live_server_url + '/')
        )

        # Re-locate the success message
        success_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
        )

        # Assert the success message and URL
        self.assertIn("Your account has been deleted!", success_message.text)
        self.assertEqual(driver.current_url, self.live_server_url + '/')
        # Take a screenshot for debugging purposes
        screenshot_path = 'eshop/test/tests_screenshots/selenium_crud_member_pics/screenshot_delete_user.png'
        driver.get_screenshot_as_file(screenshot_path)
        print(f"Screenshot saved at: {screenshot_path}")
        print("Test case for deleting user account passed successfully!")


    def tearDown(self):
        # Quit the browser after the test is complete
        self.driver.quit()