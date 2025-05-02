import os
import django

# Explicitly set the DJANGO_SETTINGS_MODULE variable at runtime if not set
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eshop.settings")
django.setup()


from django.test import TestCase, override_settings, RequestFactory
from django.urls import reverse
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from product.models import Category, Product
from member.models import Member
from cart.cart import Cart
from django.contrib.sessions.backends.db import SessionStore
from django.test import LiveServerTestCase

import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright


class MyTests(StaticLiveServerTestCase):
    def setUp(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.page.set_viewport_size({"width": 1920, "height": 1080})



    def test_user_registration_wrong_credentials_for_notmatching_password(self):
        """ Test case for wrong credentials for not matching password."""

        # Navigate to the register page
        self.page.goto(f"{self.live_server_url}/register")

        # Find and fill username/password fields
        self.page.fill("input[name='username']", "testuser")
        self.page.fill("input[name='email']", "testuser@gmail.com")
        self.page.fill("input[name='password1']", "Spezza1991?")
        self.page.fill("input[name='password2']", "Spezza")
        self.page.fill("input[name='first_name']", "AndrejTest?")
        self.page.fill("input[name='last_name']", "BanasTest?")
        self.page.fill("input[name='phone_number']", "091561714")

        # Click the login button
        self.page.click("input[value='Register']")
        time.sleep(5)

        #Wait for the error message to appear and locate it
        error_messages = self.page.locator("div.alert-error ul li").all_text_contents()
        expected_message = "The two password fields didn’t match."

        self.assertIn(expected_message, error_messages)
        self.page.screenshot(
            path="eshop/test/tests_screenshots/tests_playwright_shopping_operations/not_matching_passwords.png")
        print ("Test case for wrong credentials for not matching password successfully completed!")



    def test_user_registration_wrong_credentials_for_numeric_password(self):
        """ Test case for wrong credentials for all numeric password."""

        # Navigate to the register page
        self.page.goto(f"{self.live_server_url}/register")

        # Find and fill username/password fields
        self.page.fill("input[name='username']", "testuser")
        self.page.fill("input[name='email']", "testuser@gmail.com")
        self.page.fill("input[name='password1']", "5151651651165156")
        self.page.fill("input[name='password2']", "5151651651165156")
        self.page.fill("input[name='first_name']", "AndrejTest?")
        self.page.fill("input[name='last_name']", "BanasTest?")
        self.page.fill("input[name='phone_number']", "091561714")

        # Click the login button
        self.page.click("input[value='Register']")
        time.sleep(5)

        # Wait for the error message to appear and locate it
        error_messages = self.page.locator("div.alert-error ul li").all_text_contents()
        expected_message = "This password is entirely numeric."

        self.assertIn(expected_message, error_messages)
        self.page.screenshot(
            path="eshop/test/tests_screenshots/tests_playwright_shopping_operations/only_numeric_passwords.png")
        print("Test case for wrong credentials for all numeric password successfully completed!")

    def test_user_registration_wrong_credentials_for_numeric_and_common_password(self):
        """ Test case for wrong credentials for all numeric and common password."""

        # Navigate to the register page
        self.page.goto(f"{self.live_server_url}/register")

        # Find and fill username/password fields
        self.page.fill("input[name='username']", "testuser")
        self.page.fill("input[name='email']", "testuser@gmail.com")
        self.page.fill("input[name='password1']", "123456789")
        self.page.fill("input[name='password2']", "123456789")
        self.page.fill("input[name='first_name']", "AndrejTest?")
        self.page.fill("input[name='last_name']", "BanasTest?")
        self.page.fill("input[name='phone_number']", "091561714")

        # Click the login button
        self.page.click("input[value='Register']")
        time.sleep(5)

        # Wait for the error message to appear and locate it
        error_messages = self.page.locator("div.alert-error ul li").all_text_contents()
        expected_message1 = "This password is entirely numeric."
        expected_message2 = "This password is too common."

        self.assertIn(expected_message1, error_messages)
        self.assertIn(expected_message2, error_messages)
        self.page.screenshot(
            path="eshop/test/tests_screenshots/tests_playwright_shopping_operations/only_numeric_passwords.png")
        print("Test case for wrong credentials for all numeric and common password successfully completed!")



    def test_user_registration_wrong_credentials_for_short_password(self):
        """ Test case for wrong credentials for password too short."""

        # Navigate to the register page
        self.page.goto(f"{self.live_server_url}/register")

        # Find and fill username/password fields
        self.page.fill("input[name='username']", "testuser")
        self.page.fill("input[name='email']", "testuser@gmail.com")
        self.page.fill("input[name='password1']", "Spezza")
        self.page.fill("input[name='password2']", "Spezza")
        self.page.fill("input[name='first_name']", "AndrejTest?")
        self.page.fill("input[name='last_name']", "BanasTest?")
        self.page.fill("input[name='phone_number']", "091561714")


        # Click the login button
        self.page.click("input[value='Register']")
        time.sleep(5)

        # Wait for the error message to appear and locate it
        error_messages = self.page.locator("div.alert-error ul li").all_text_contents()
        expected_message = "This password is too short. It must contain at least 8 characters."

        self.assertIn(expected_message, error_messages)
        self.page.screenshot(
            path="eshop/test/tests_screenshots/tests_playwright_shopping_operations/too_short_passwords.png")
        print("Test case for wrong credentials for short password password successfully completed!")



    def test_user_registration_missing_credentials_for_registration(self):
        """ Test case for wrong credentials for missing credentials."""

        # Navigate to the register page
        self.page.goto(f"{self.live_server_url}/register")

        # Find and fill username/password fields
        self.page.fill("input[name='username']", "testuser")
        self.page.fill("input[name='email']", "")
        self.page.fill("input[name='password1']", "Spezza1991|????")
        self.page.fill("input[name='password2']", "Spezza1991|????")
        self.page.fill("input[name='first_name']", "?")
        self.page.fill("input[name='last_name']", "")
        self.page.fill("input[name='phone_number']", "091561714")

        # Click the login button
        self.page.click("input[value='Register']")
        time.sleep(5)

        # Wait for the error message to appear and locate it
        error_messages = self.page.locator("div.alert-error ul li").all_text_contents()
        expected_message = "This field is required."

        self.assertIn(expected_message, error_messages)
        self.page.screenshot(
            path="eshop/test/tests_screenshots/tests_playwright_shopping_operations/missing_registration_data.png")
        print("Test case for missing credentials for registration successfully completed!")



    def test_user_successful_registration(self):
        """ Test case for successful registration process."""

        # Navigate to the register page
        self.page.goto(f"{self.live_server_url}/register")

        # Find and fill username/password fields
        self.page.fill("input[name='username']", "testuser")
        self.page.fill("input[name='email']", "test@gmail.com")
        self.page.fill("input[name='password1']", "Spezza1991?")
        self.page.fill("input[name='password2']", "Spezza1991?")
        self.page.fill("input[name='first_name']", "AndrejTest")
        self.page.fill("input[name='last_name']", "BanasTest")
        self.page.fill("input[name='phone_number']", "091561714")

        # Click the login button
        self.page.click("input[value='Register']")
        time.sleep(5)

        # Wait for the error message to appear and locate it
        error_messages = self.page.locator("div.alert-error ul li").all_text_contents()



        self.assertEqual(len(error_messages), 0)
        print("Redirected to the Login url!")
        current_url = self.page.url  # Get the current page URL
        expected_url = f"{self.live_server_url}/login"  # Define the URL you expect to redirect to
        self.assertEqual(expected_url, current_url)  # Assert that the redirect happened to the correct URL
        print("Test case for registration successfully completed!")
        self.page.screenshot(
            path="eshop/test/tests_screenshots/tests_playwright_shopping_operations/successful_registration.png")
        print("Redirected to the Login url!")



    def test_user_login_with_wrong_credentials(self):
        """ Test case for login with incorrect credentials."""

        # Navigate to the register page
        self.page.goto(f"{self.live_server_url}/login")

        # Find and fill username/password fields
        self.page.fill("input[name='username']", "testuser")
        self.page.fill("input[name='password']", "Spezza")

        # Click the login button
        self.page.click("input[value='Login']")

        # Wait for the error message to appear and locate it
        error_messages = self.page.locator("ul.errorlist li").all_text_contents()

        # Assert the error message content
        expected_message = "Please enter a correct username and password. Note that both fields may be case-sensitive."
        self.assertIn(expected_message, error_messages)
        print("Test case for login with incorrect credentials successfully completed!")
        self.page.screenshot(
            path="eshop/test/tests_screenshots/tests_playwright_shopping_operations/login_with_incorrect_credentials.png")
        print("Redirected to the Login url!")



    def test_user_login_and_logout_successful(self):
        """ Test case for login with correct credentials."""

        # Navigate to the register page and create user instance
        self.page.goto(f"{self.live_server_url}/register")

        # Find and fill username/password fields
        self.page.fill("input[name='username']", "testuser")
        self.page.fill("input[name='email']", "test@gmail.com")
        self.page.fill("input[name='password1']", "Spezza1991?")
        self.page.fill("input[name='password2']", "Spezza1991?")
        self.page.fill("input[name='first_name']", "AndrejTest")
        self.page.fill("input[name='last_name']", "BanasTest")
        self.page.fill("input[name='phone_number']", "091561714")

        # Click the login button
        self.page.click("input[value='Register']")
        time.sleep(5)
        print("User created and redirected to login page!")

        # Navigate to the login page
        self.page.goto(f"{self.live_server_url}/login")
        time.sleep(5)

        # Find and fill username/password fields
        self.page.fill("input[name='username']", "testuser")
        self.page.fill("input[name='password']", "Spezza1991?")

        # Click the login button
        self.page.click("input[value='Login']")

        current_url = self.page.url  # Get the current page URL
        expected_url = f"{self.live_server_url}/dashboard"  # Define the URL you expect to redirect to
        self.assertEqual(expected_url, current_url)  # Assert that the redirect happened to the correct URL
        print("Logged in with success and redirected to the Dashboard url!")

        # Click the login button
        self.page.locator("#Logout").click()
        time.sleep(5)

        error_messages = self.page.locator("div.alert-success").all_text_contents()
        cleaned_error_messages = [message.strip() for message in error_messages]
        expected_message = "You logged out successfully"

        self.assertIn(expected_message, cleaned_error_messages[0])

        current_url = self.page.url  # Get the current page URL
        expected_url = f"{self.live_server_url}/"  # Define the URL you expect to redirect to
        self.assertEqual(expected_url, current_url)

        print("Test case for login with incorrect credentials successfully completed!")
        self.page.screenshot(
            path="eshop/test/tests_screenshots/tests_playwright_shopping_operations/login_with_incorrect_credentials.png")


    def tearDown(self):
        self.browser.close()
        self.playwright.stop()

