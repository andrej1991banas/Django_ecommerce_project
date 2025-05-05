from django.test import TestCase
from django.urls import reverse
from product.models import Product
from cart.cart import Cart
from product.models import Category
from member.models import Member
from django.contrib.auth.models import User
from order.forms import ShippingAddressForm,PaymentForm


class UnauthenticatedUserTestCase(TestCase):
    def setUp(self):
        """Set up initial data for testing"""
        #category creation
        self.category = Category.objects.create(name="Category A")
        # Create products
        self.product1 = Product.objects.create(category=self.category,brand="TestbrandA", model="Product A", price=10.0 )
        self.product2 = Product.objects.create(category=self.category, brand="TestbrandB",model="Product B", price=20.0)
        self.cart_add_url = reverse("cart-add")


    def test_render_products(self):
        """ Test case for rendering the page with products"""
        # Test to ensure products can be viewed
        response = self.client.get(reverse("show-products"))  # Define your product list URL
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product1.model)
        self.assertContains(response, self.product2.model)
        print("Test case for rendering the page with products successfully completed!")


    def test_add_to_cart(self):
        """ Test case for adding a product to the cart."""
        # Simulate adding a product to the cart
        response = self.client.post(self.cart_add_url, {
            'action': 'post',
            'product_id': self.product1.id,  # Set product ID
            'product_qty': 2,  # Set quantity
        })

        # Check the JSON response for cart quantity
        self.assertIn("qty", response.json())
        self.assertEqual(response.json()["qty"], 1)  # Ensure quantity matches
        print(" Successfully added product to the cart and updated number of items inside the cart")

        # Verify the cart contents (from session) and verify it is not empty
        cart= Cart(self.client) #getting cart instance
        self.assertTrue(cart.__len__() > 0)
        cart_products = cart.get_cart_prods()
        self.assertEqual(len(cart_products), 1)
        print ("Cart has one item in it.")

        cart_content = list(cart.cart.items())
        self.assertEqual(cart_content[0] , (str(self.product1.id),2))

        # Check the product and quantity in the cart
        cart_items = list(cart.cart.values())  # Retrieve the items in the cart
        self.assertEqual(len(cart_items), 1)  # Ensure there is only one item in the cart
        self.assertEqual(cart_items[0], 2)  # Match product quantity
        print ("Cart instance returning dict with id of the product and quantity.")

        print ("Test case for adding a product to the cart successfully completed!")


    def test_update_cart_check_total(self):
        """ Test case for updating the cart quantities and checking the total price."""
        # Add to cart first
        response = self.client.post(self.cart_add_url, {
                    'action': 'post',
                    'product_id': self.product1.id,  # Set product ID
                    'product_qty': 2,  # Set quantity
                })

        cart = Cart(self.client)  # getting cart instance
        cart_qty = list(cart.cart.values())[0]
        self.assertEqual(cart_qty, 2)
        print ("Cart has quantity of 2 items in it.")

        # Update the cart quantity
        response = self.client.post(reverse("cart-update"), {
                    'action': 'post',
                    "product_id": self.product1.id,
                    "product_qty": 5
                })
        # Check the JSON response for cart quantity
        self.assertIn("quantity", response.json())

        # # Verify the updated quantity
        cart= Cart(self.client) #getting cart instance
        cart_qty = list(cart.cart.values())[0]
        self.assertEqual (cart_qty,5)
        print("Cart has updated quantity of 5 items in it.")

        totals = cart.cart_total() #call the cart_total to get total price of the cart
        self.assertEqual(totals.amount, 50.00) #total count as qty*price
        print ("Test case for updating the cart quantities and checking the total price successfully completed!")


    def test_delete_cart(self):
        """ Test case for updating the cart quantities and checking the total price."""
        # Add to cart first
        self.client.post(self.cart_add_url, {
                    'action': 'post',
                    'product_id': self.product1.id,  # Set product ID
                    'product_qty': 2,  # Set quantity
                })

        self.client.post(self.cart_add_url, {
            'action': 'post',
            'product_id': self.product2.id,  # Set product ID
            'product_qty': 3,  # Set quantity
        })


        self.assertEqual
        cart = Cart(self.client)  # getting cart instance

        self.assertTrue(cart.__len__() == 2) #the products is in the cart
        print ("Cart has 2 items in it.")

        # Delete item from the cart
        response = self.client.post(reverse("cart-delete"), {
                    'action': 'post',
                    "product_id": self.product1.id
                })
        self.assertNotIn(self.product1.id, response.json())
        print ("Product 1 was deleted from the cart.")
        print (" Test case for deleting the cart item successfully completed!")


    def test_checkout(self):
        """Test the checkout process, including filling the form."""
        # Add to cart first
        self.client.post(self.cart_add_url, {
                    'action': 'post',
                    'product_id': self.product1.id,  # Set product ID
                    'product_qty': 2,  # Set quantity
                })


        # Proceed to checkout
        response = self.client.post(reverse("checkout"))
        self.assertEqual(response.status_code, 200)
        print ("Checkout page was successfully loaded")

        #Submit shipping data to the form
        shipping_data = {
            'shipping_first_name': 'John',
            'shipping_last_name': 'Doe',
            'shipping_email' : 'test@gmail.com',
            'shipping_address1': '123 Main Street',
            'shipping_city': 'New York',
            'shipping_zipcode': '10001',
            'shipping_country': 'US',
        }
        #Check if the form submission redirects successfully
        response = self.client.post(reverse("checkout"), data=shipping_data)

        self.assertEqual(response.status_code, 302)  # Expect redirect
        print(f"Redirection response is {response.url}")
        self.assertEqual(response.url, reverse("billing-info"))
        print("Test case for checkout successfully completed and redirected to billing info page!")


    def test_order_creation(self):
        """Test creating an order."""
        # Add to cart first
        self.client.post(self.cart_add_url, {
            'action': 'post',
            'product_id': self.product1.id,  # Set product ID
            'product_qty': 2,  # Set quantity
        })

        # Proceed to payment info page
        response = self.client.post(reverse("checkout"))
        self.assertEqual(response.status_code, 200)

        #submit payment form with data
        shipping_data = {
            'shipping_first_name': 'John',
            'shipping_last_name': 'Doe',
            'shipping_email': 'test@gmail.com',
            'shipping_address1': '123 Main Street',
            'shipping_city': 'New York',
            'shipping_zipcode': '10001',
            'shipping_country': 'US',
        }



class AuthenticatedUserTestCase(TestCase):
    def setUp(self):
        """Set up initial data for testing"""
        #category creation
        self.category = Category.objects.create(name="Category A")
        # Create products
        self.product1 = Product.objects.create(category=self.category,brand="TestbrandA", model="Product A", price=10.0 )
        self.product2 = Product.objects.create(category=self.category, brand="TestbrandB",model="Product B", price=20.0)
        self.cart_add_url = reverse("cart-add")

        """Setup pre-test data for the test case"""
        # Create User for Member
        self.user = User.objects.create_user(username="andrejtest", password="password123", first_name="Testandrej",
                                             last_name="Test",
                                             email="andrej@test.com")

        # Create Member object with test data
        self.member = Member.objects.create(
            user=self.user,
            email="andrej@test.com",
            first_name="Testandrej",
            last_name="Test",
            gender="Male",
            phone_number="123456789",
            city="TestCity",
            country="USA")
        print("Initialize Member model for testing")

        self.client.login(username="andrejtest", password="password123")


    def test_add_to_cart(self):
        """ Test case for adding a product to the cart."""
        # Simulate adding a product to the cart
        response = self.client.post(self.cart_add_url, {
            'action': 'post',
            'product_id': self.product1.id,  # Set product ID
            'product_qty': 2,  # Set quantity
        })

        self.assertEqual(response.status_code, 200)  # Ensure the response status is OK

        # Check the JSON response for cart quantity
        self.assertIn("qty", response.json())
        self.assertEqual(response.json()["qty"], 1)  # Ensure quantity matches
        print(" Successfully added product to the cart and updated number of items inside the cart")

        # Verify the cart contents (from session) and verify it is not empty
        cart= Cart(self.client) #getting cart instance
        self.assertTrue(cart.__len__(), 1)

        print ("Cart has one item in it.")

        cart_content = list(cart.cart.items())
        self.assertEqual(cart_content[0] , (str(self.product1.id),2))

        # Check the product and quantity in the cart
        cart_items = list(cart.cart.values())  # Retrieve the items in the cart
        self.assertEqual(len(cart_items), 1)  # Ensure there is only one item in the cart
        self.assertEqual(cart_items[0], 2)  # Match product quantity
        print ("Cart instance returning dict with id of the product and quantity.")

        print ("Test case for adding a product to the cart successfully completed!")


    def test_update_cart_check_total(self):
        """ Test case for updating the cart quantities and checking the total price."""
        # Add to cart first
        response = self.client.post(self.cart_add_url, {
                    'action': 'post',
                    'product_id': self.product1.id,  # Set product ID
                    'product_qty': 2,  # Set quantity
                })

        cart = Cart(self.client)  # getting cart instance
        cart_qty = list(cart.cart.values())[0]
        self.assertEqual(cart_qty, 2)
        print ("Cart has quantity of 2 items in it.")

        # Update the cart quantity
        response = self.client.post(reverse("cart-update"), {
                    'action': 'post',
                    "product_id": self.product1.id,
                    "product_qty": 5
                })
        # Check the JSON response for cart quantity
        self.assertIn("quantity", response.json())

        # # Verify the updated quantity
        cart= Cart(self.client) #getting cart instance
        cart_qty = list(cart.cart.values())[0]
        self.assertEqual (cart_qty,5)
        print("Cart has updated quantity of 5 items in it.")

        totals = cart.cart_total() #call the cart_total to get total price of the cart
        self.assertEqual(totals.amount, 50.00) #total count as qty*price
        print ("Test case for updating the cart quantities and checking the total price successfully completed!")


    def test_delete_cart(self):
        """ Test case for updating the cart quantities and checking the total price."""
        # Add to cart first
        self.client.post(self.cart_add_url, {
                    'action': 'post',
                    'product_id': self.product1.id,  # Set product ID
                    'product_qty': 2,  # Set quantity
                })

        self.client.post(self.cart_add_url, {
            'action': 'post',
            'product_id': self.product2.id,  # Set product ID
            'product_qty': 3,  # Set quantity
        })


        self.assertEqual
        cart = Cart(self.client)  # getting cart instance

        self.assertTrue(cart.__len__() == 2) #the products is in the cart
        print ("Cart has 2 items in it.")

        # Delete item from the cart
        response = self.client.post(reverse("cart-delete"), {
                    'action': 'post',
                    "product_id": self.product1.id
                })
        self.assertNotIn(self.product1.id, response.json())
        print ("Product 1 was deleted from the cart.")
        print (" Test case for deleting the cart item successfully completed!")


    def test_checkout(self):
        """Test the checkout process, including filling the form."""
        # Add to cart first
        self.client.post(self.cart_add_url, {
                    'action': 'post',
                    'product_id': self.product1.id,  # Set product ID
                    'product_qty': 2,  # Set quantity
                })


        # Proceed to checkout
        response = self.client.post(reverse("checkout"))
        self.assertEqual(response.status_code, 200)
        print ("Checkout page was successfully loaded")

        #Submit shipping data to the form
        shipping_data = {
            'shipping_first_name': 'John',
            'shipping_last_name': 'Doe',
            'shipping_email' : 'test@gmail.com',
            'shipping_address1': '123 Main Street',
            'shipping_city': 'New York',
            'shipping_zipcode': '10001',
            'shipping_country': 'US',
        }
        #Check if the form submission redirects successfully
        response = self.client.post(reverse("checkout"), data=shipping_data)

        self.assertEqual(response.status_code, 302)  # Expect redirect
        print(f"Redirection response is {response.url}")
        self.assertEqual(response.url, reverse("billing-info"))
        print("Test case for checkout successfully completed and redirected to billing info page!")


    def test_order_creation(self):
        """Test creating an order."""
        # Add to cart first
        self.client.post(self.cart_add_url, {
            'action': 'post',
            'product_id': self.product1.id,  # Set product ID
            'product_qty': 2,  # Set quantity
        })

        # Proceed to payment info page
        response = self.client.post(reverse("checkout"))
        self.assertEqual(response.status_code, 200)

        #submit payment form with data
        shipping_data = {
            'shipping_first_name': 'John',
            'shipping_last_name': 'Doe',
            'shipping_email': 'test@gmail.com',
            'shipping_address1': '123 Main Street',
            'shipping_city': 'New York',
            'shipping_zipcode': '10001',
            'shipping_country': 'US',
        }



class PaymentFormTest(TestCase):
    def setUp(self):
        # Define valid form data to reuse in each test
        self.valid_form_data = {
            'card_name': 'John Doe',
            'card_number': '4111111111111111',  # Example valid card number
            'card_exp_date': '12/25',  # Example of expiration date in MM/YY format
            'card_cvv_number': '123',
            'card_address1': '123 Main St',
            'card_address2': '',
            'card_city': 'New York',
            'card_state': 'NY',
            'card_zipcode': '10001',
            'card_country': 'US',
        }


    def test_payment_form_valid(self):
        """Test that the form is valid with all valid data"""
        form = PaymentForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid(), form.errors)
        print ("Test case for payment form with all valid data successfully completed!")


    def test_payment_form_missing_required_fields(self):
        """Test that the form is invalid if required fields are missing"""

        # Remove required fields one by one and test each case
        required_fields = ['card_name', 'card_number', 'card_exp_date', 'card_cvv_number',
                           'card_address1', 'card_city', 'card_zipcode', 'card_country']

        for field in required_fields:
            invalid_data = self.valid_form_data.copy()
            invalid_data.pop(field)  # Remove the required field
            form = PaymentForm(data=invalid_data)
            self.assertFalse(form.is_valid())
            self.assertIn(field, form.errors)  # Check that the missing field is in the form errors
        print ("Test case for payment form with missing required fields successfully completed!")


    def test_payment_form_optional_fields_blank(self):
        """Test that the form is valid with optional fields left blank"""

        # Set optional fields to blank
        valid_data = self.valid_form_data.copy()
        valid_data['card_address2'] = ''
        valid_data['card_state'] = ''
        form = PaymentForm(data=valid_data)
        self.assertTrue(form.is_valid(), form.errors)
        print (" Test case for payment form with optional fields blank successfully completed!")
#


class ShippingAddressFormTest(TestCase):
    def setUp(self):
        # Define valid form data to reuse in each test
        self.valid_form_data = {
            'shipping_first_name': 'Andrej',
            'shipping_last_name': 'Banas',  # Example valid card number
            'shipping_email': 'test@gmail.com',  # Example of expiration date in MM/YY format
            'shipping_address1': 'Brezova',
            'shipping_address2': '523/29',
            'shipping_city': 'Bratislava',
            'shipping_state': 'Zapad',
            'shipping_zipcode': '00001',
            'shipping_country': 'USA',
        }


    def test_payment_form_valid(self):
        """Test that the form is valid with all valid data"""
        form = ShippingAddressForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid(), form.errors)
        print ("Test case for shipping address form with all valid data successfully completed!")


    def test_payment_form_missing_required_fields(self):
        """Test that the form is invalid if required fields are missing"""
        #Remove required fields one by one and test each case
        required_fields = ['shipping_first_name', 'shipping_last_name', 'shipping_state', 'shipping_zipcode',
                       'shipping_country','shipping_address1','shipping_city','shipping_email', 'shipping_email']

        for field in required_fields:
            invalid_data = self.valid_form_data.copy()
            invalid_data.pop(field)  # Remove the required field
            form = ShippingAddressForm(data=invalid_data)

        self.assertFalse(form.is_valid())
        self.assertIn(field, form.errors)  # Check that the missing field is in the form errors
        print ("Test case for payment form with missing required fields successfully completed!")


    def test_payment_form_optional_fields_blank(self):
        """Test that the form is valid with optional fields left blank"""

        # Set optional fields to blank
        valid_data = self.valid_form_data.copy()
        valid_data['shipping_address2'] = ''
        valid_data['shipping_state'] = ''
        form = ShippingAddressForm(data=valid_data)
        self.assertTrue(form.is_valid(), form.errors)
        print (" Test case for payment form with optional fields blank successfully completed!")

