import unittest
from product.models import Product
from cart.cart import Cart
from product.models import Category
from member.models import Member
from django.contrib.messages import get_messages
from order.models import ShippingAddress
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from order.models import Order, OrderItems
from django.http import HttpRequest
from djmoney.money import Money
from django.utils.timezone import now






class OrderProcessTestCase(TestCase):
    def setUp(self):
        """Set up initial data for testing"""
        #category creation
        self.category = Category.objects.create(name="Category A")
        # Create products
        self.product1 = Product.objects.create(category=self.category,brand="TestbrandA", model="Product A", price=10.0, image="test.jpg" )
        self.product2 = Product.objects.create(category=self.category, brand="TestbrandB",model="Product B", price=20.0, image="test.jpg")
        self.cart_add_url = reverse("cart-add")


        #create User and Member
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
            country="USA",
            old_cart ='{"1": 2,"2": 1,}')
        print("Initialize Member model for testing")

        #Create Cart instance
        self.cart ={"1":2, "2":1}


        # create shipping address for User
        self.shipping_address = ShippingAddress.objects.create(
            shipping_user=self.user,
            shipping_first_name='Andrej',
            shipping_last_name='Banas',  # Example valid card number
            shipping_email='test@gmail.com',  # Example of expiration date in MM/YY format
            shipping_address1='Brezova',
            shipping_address2='523/29',
            shipping_city='Bratislava',
            shipping_state='Zapad',
            shipping_zipcode='00001',
            shipping_country='USA', )
        print("Initialize ShippingAddress model for testing")


        # self.client.login(username="andrejtest", password="password123")


        #create SuperUser
        self.superuser = User.objects.create_superuser(username="superuser", password="password123", first_name="Super",)
        print("Initialize SuperUser model for testing")



    def test_billing_info_page_without_post_request(self):
        """ Test case for billing info page"""
        response = self.client.get(reverse("billing-info"))

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))  # Ensure the expected redirection
        self.assertEqual(str(messages[0]), "Access Denied")
        print("Test case for billing info page successfully completed!")


    def test_billing_info_page_with_non_auth_user(self):
        """Test case for billing_info view with non-authenticated user using POST request"""
        client = Client()
        # Add to cart first
        self.client.post(self.cart_add_url, {
            'action': 'post',
            'product_id': self.product1.id,  # Set product ID
            'product_qty': 2,  # Set quantity
        })

        # Construct POST data for request
        post_data = {
            "shipping_first_name": "John",
            "shipping_last_name": "Doe",
            "shipping_email": "john.doe@example.com",
            "shipping_address1": "123 Test Street",
            "shipping_address2": "",
            "shipping_city": "New York",
            "shipping_state": "NY",
            "shipping_zipcode": "10001",
            "shipping_country": "USA",
        }

        # Simulate POST request to the billing_info endpoint
        response = client.post(reverse("billing-info"), data=post_data)

        # Assert that the status code is 200 (indicates the page rendered successfully)
        self.assertEqual(response.status_code, 200)

        # Check if the session was updated correctly with `my_shipping` data
        session_data = client.session.get("my_shipping")
        self.assertIsNotNone(session_data)
        self.assertEqual(session_data["shipping_first_name"], "John")
        self.assertEqual(session_data["shipping_city"], "New York")
        print("Session updated successfully with shipping information!")

        cart = Cart(self.client)
        prods = cart.get_cart_qty()
        self.assertEqual({"1": 2}, prods)
        print("Cart product data retrieved successfully!")

        print("Test case for billing_info view with non-authenticated user completed successfully!")


    def test_billing_info_authenticated_user(self):
        """Test case for billing_info view with authenticated user using POST request"""
        # Create a test client and log in an authenticated user
        client = Client()

        client.login(username="andrejtest", password="password123")
        self.assertTrue(self.user.is_authenticated)

        # Add to cart first
        self.client.post(self.cart_add_url, {
            'action': 'post',
            'product_id': self.product1.id,  # Set product ID
            'product_qty': 2,  # Set quantity
        })


        # Construct POST data for request
        post_data = {
            "shipping_first_name": "John",
            "shipping_last_name": "Doe",
            "shipping_email": "john.doe@example.com",
            "shipping_address1": "123 Test Street",
            "shipping_address2": "",
            "shipping_city": "New York",
            "shipping_state": "NY",
            "shipping_zipcode": "10001",
            "shipping_country": "USA",
        }

        # Simulate POST request to the billing_info endpoint
        response = client.post(reverse("billing-info"), data=post_data)

        # Assert that the status code is 200 (indicates the page rendered successfully)
        self.assertEqual(response.status_code, 200)

        # Check if the session was updated correctly with `post_data` data
        session_data = client.session.get("my_shipping")
        self.assertIsNotNone(session_data)
        self.assertEqual(session_data["shipping_first_name"], "John")
        self.assertEqual(session_data["shipping_city"], "New York")
        print("Session updated successfully with shipping information!")


        # Assert that the `member` object was retrieved and its field is in the context
        self.assertIn("member", response.context)
        self.assertEqual(response.context["member"], self.member.phone_number)
        print("Member data retrieved and included in context successfully!")

        cart = Cart(self.client)
        prods = cart.get_cart_qty()
        print (prods)

        self.assertEqual({"1":2}, prods)

        print("Cart product data retrieved successfully!")
        print("Test case for billing_info view with authenticated user completed successfully!")

    def test_billing_info_page_without_post_request(self):
        """ Test case for process order view """
        response = self.client.get(reverse("process-order"))

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))  # Ensure the expected redirection
        self.assertEqual(str(messages[0]), "Access Denied")
        print("Test case for billing info page successfully completed!")


class OrderProcessAuthenticatedUserTestCase(TestCase):
    def setUp(self):
        # Create a superuser
        self.user = User.objects.create_superuser(
            username="andrejtest",
            password="password123",
            email="andrejtest@example.com"
        )
        # Create a Member instance for the superuser
        self.member = Member.objects.create(user=self.user)

        # Category creation
        self.category = Category.objects.create(name="Category A")

        # Create a test product
        self.product1 = Product.objects.create(
            category=self.category,
            brand="TestbrandA",
            model="Product A",
            price=Money(10.00, 'EUR'),
            image="test.jpg"
        )

        # URLs
        self.payment_info_url = reverse("payment-info")
        self.process_order_url = reverse("process-order")
        self.order_complete_url = reverse("index")

        # Create a test client and log in
        self.client = Client()
        self.client.login(username="andrejtest", password="password123")

        # Manually set up session data
        session = self.client.session
        session['my_shipping'] = {
            'shipping_first_name': 'John',
            'shipping_last_name': 'Doe',
            'shipping_email': 'john.doe@example.com',
            'shipping_address1': '123 Test Street',
            'shipping_address2': '',
            'shipping_city': 'New York',
            'shipping_state': 'NY',
            'shipping_zipcode': '10001',
            'shipping_country': 'USA'
        }

        session['session_key'] = {str(self.product1.id): 2}  # Cart data
        session.save()

    def test_billing_info_authenticated_user(self):
        """Test case for process order view order creation view with authenticated user using POST request"""
        super().setUp()

        # Verify user is authenticated and a superuser
        self.assertTrue(self.user.is_authenticated)
        self.assertTrue(self.user.is_superuser)

        # Verify cart contents
        request = HttpRequest()
        request.session = self.client.session
        request.user = self.user
        cart = Cart(request)
        self.assertEqual(cart.get_cart_qty()[str(self.product1.id)], 2)
        self.assertEqual(cart.cart_total().amount, 20.00)
        self.assertEqual(cart.cart_total().currency.code, 'EUR')

        # Simulate GET request to payment-info
        response = self.client.get(self.payment_info_url)
        self.assertEqual(response.status_code, 200)  # Expect form page to render

        # Construct payment POST data
        post_data = {
            'card_name': 'John Doe',
            'card_number': '4111111111111111',
            'card_exp_date': '12/25',
            'card_cvv_number': '123',
            'card_address1': '123 Main St',
            'card_address2': '',
            'card_city': 'New York',
            'card_state': 'NY',
            'card_zipcode': '10001',
            'card_country': 'US',
        }

        # Simulate POST request to payment-info
        response = self.client.post(self.payment_info_url, data=post_data)
        print ("Successfully updated payment form iwth valid data")
        # Assert that the status code is 200 (indicates the page rendered successfully)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(self.process_order_url, data=self.client.session)
        print ("Successfully used payment form to process order and create order and order items in database")

        self.assertEqual(response.status_code, 200)

        # Verify the Order was created
        order = Order.objects.filter(email='john.doe@example.com').first()

        self.assertEqual(order.full_name, "John' 'Doe")
        # self.assertEqual(order.amount_paid, 20.00)
        self.assertEqual(order.member.count(), 1)
        self.assertEqual(order.member.first(), self.member)

        # Verify OrderItems were created
        order_items = OrderItems.objects.filter(order=order)
        self.assertEqual(order_items.count(), 1)
        order_item = order_items.first()
        self.assertEqual(order_item.products, self.product1)
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.price.amount, 10.00)

        # Verify cart session was cleared
        self.assertNotIn(f'session_key_{self.product1.id}', self.client.session)

        # Verify old_cart field was cleared
        self.member.refresh_from_db()
        self.assertEqual(self.member.old_cart, "")
        print ("Test case for creating order with authenticated user completed successfully!")

class OrderProcessNonAuthenticatedUserTestCase(TestCase):
    def setUp(self):
        # Category creation
        self.category = Category.objects.create(name="Category A")

        # Create a test product
        self.product1 = Product.objects.create(
            category=self.category,
            brand="TestbrandA",
            model="Product A",
            price=Money(10.00, 'EUR'),
            image="test.jpg"
        )

        # URLs
        self.payment_info_url = reverse("payment-info")
        self.process_order_url = reverse("process-order")
        self.order_complete_url = reverse("index")

        # Create a test client and log in
        self.client = Client()


        # Manually set up session data
        session = self.client.session
        session['my_shipping'] = {
            'shipping_first_name': 'John',
            'shipping_last_name': 'Doe',
            'shipping_email': 'john.doe@example.com',
            'shipping_address1': '123 Test Street',
            'shipping_address2': '',
            'shipping_city': 'New York',
            'shipping_state': 'NY',
            'shipping_zipcode': '10001',
            'shipping_country': 'USA'
        }

        session['session_key'] = {str(self.product1.id): 2}  # Cart data
        session.save()

    def test_billing_info_non_authenticated_user(self):
        """Test case for process order view with non authenticated user using POST request"""
        super().setUp()


        # Verify cart contents
        request = HttpRequest()
        request.session = self.client.session

        cart = Cart(request)
        self.assertEqual(cart.get_cart_qty()[str(self.product1.id)], 2)
        self.assertEqual(cart.cart_total().amount, 20.00)
        self.assertEqual(cart.cart_total().currency.code, 'EUR')

        # Simulate GET request to payment-info
        response = self.client.get(self.payment_info_url)
        self.assertEqual(response.status_code, 200)  # Expect form page to render

        # Construct payment POST data
        post_data = {
            'card_name': 'John Doe',
            'card_number': '4111111111111111',
            'card_exp_date': '12/25',
            'card_cvv_number': '123',
            'card_address1': '123 Main St',
            'card_address2': '',
            'card_city': 'New York',
            'card_state': 'NY',
            'card_zipcode': '10001',
            'card_country': 'US',
        }

        # Simulate POST request to payment-info
        response = self.client.post(self.payment_info_url, data=post_data)
        print("Successfully updated payment form iwth valid data")
        # Assert that the status code is 200 (indicates the page rendered successfully)
        self.assertEqual(response.status_code, 302)
        print (self.client.session)
        response = self.client.post(self.process_order_url, data=self.client.session)
        print("Successfully used payment form to process order and create order and order items in database")

        self.assertEqual(response.status_code, 200)
        # Verify the Order was created
        order = Order.objects.filter(email='john.doe@example.com').first()

        self.assertEqual(order.full_name, "John' 'Doe")
        # self.assertEqual(order.amount_paid, 20.00)

        # Verify OrderItems were created
        order_items = OrderItems.objects.filter(order=order)
        self.assertEqual(order_items.count(), 1)
        order_item = order_items.first()
        self.assertEqual(order_item.products, self.product1)
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.price.amount, 10.00)

        # Verify cart session was cleared
        self.assertNotIn(f'session_key_{self.product1.id}', self.client.session)

        self.assertEqual(response.status_code, 200)
        print("Test case for creating order with non authenticated user completed successfully!")


class OrderStatusCheckAndUpdateTestCase(TestCase):
    def setUp(self):
        # Create a superuser
        self.user = User.objects.create_superuser(
            username="andrejtest",
            password="password123",
            email="andrejtest@example.com"
        )
        # Create a Member instance for the superuser
        self.member = Member.objects.create(user=self.user)

        # Category creation
        self.category = Category.objects.create(name="Category A")

        # Create a test product
        self.product1 = Product.objects.create(
            category=self.category,
            brand="TestbrandA",
            model="Product A",
            price=Money(10.00, 'EUR'),
            image="test.jpg"
        )

        # URLs
        self.payment_info_url = reverse("payment-info")
        self.process_order_url = reverse("process-order")
        self.order_complete_url = reverse("index")

        # Create a test client and log in
        self.client = Client()
        self.client.login(username="andrejtest", password="password123")

        # Manually set up session data
        session = self.client.session
        session['my_shipping'] = {
            'shipping_first_name': 'John',
            'shipping_last_name': 'Doe',
            'shipping_email': 'john.doe@example.com',
            'shipping_address1': '123 Test Street',
            'shipping_address2': '',
            'shipping_city': 'New York',
            'shipping_state': 'NY',
            'shipping_zipcode': '10001',
            'shipping_country': 'USA'
        }

        session['session_key'] = {str(self.product1.id): 2}  # Cart data
        session.save()

        self.order = Order.objects.create(
            # Note: Many-to-many fields (e.g., member) must be added separately after creation
            full_name="John Doe",
            email="john.doe@example.com",
            shipping_label="123 Test Street\n\nNew York\nNY\n10001\nUSA",
            amount_paid=Money(20.00, 'EUR'),
            created_at="2023-10-01 12:00:00",
            status=False,
            date_shipped=None)

        # Add members to the order
        self.order.member.add(self.member)


    def tests_order_status_check_and_update(self):
        """Test case for order status check view with authenticated user using POST request"""
        super().setUp()

        # Verify user is authenticated and a superuser
        self.assertTrue(self.user.is_authenticated)
        self.assertTrue(self.user.is_superuser)

        order = Order.objects.filter(email='john.doe@example.com').first()
        self.assertEqual(order.status, False)
        self.assertEqual(order.date_shipped, None)

        order.status = True
        order.save()

        # Reload the order from the database to reflect any changes made by the signal
        order.refresh_from_db()

        # Assert the changes
        self.assertTrue(order.status)  # Status should now be True
        self.assertIsNotNone(order.date_shipped)  # Shipping date should be automatically set
        self.assertTrue(
            (now() - order.date_shipped).total_seconds() < 1)  # Check if the date is set to approximately now
        """ I have to assert shipped date just approximately as my script set the time to now, the instance of changing the
        order status."""
        print("Test case for order status update and auto-shipped date completed successfully!")


class OrderDetailsViewTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        # Create a Member instance for the superuser
        self.member = Member.objects.create(user=self.user)

        self.client = Client()

        # Category creation
        self.category = Category.objects.create(name="Category A")

        # Create a test product
        self.product = Product.objects.create(
            category=self.category,
            brand="TestbrandA",
            model="Product A",
            price=Money(10.00, 'EUR'),
            image="test.jpg")

        self.order = Order.objects.create(
        # Note: Many-to-many fields (e.g., member) must be added separately after creation
        full_name="John Doe",
        email="john.doe@example.com",
        shipping_label="123 Test Street\n\nNew York\nNY\n10001\nUSA",
        amount_paid=Money(20.00, 'EUR'),
        created_at="2023-10-01 12:00:00",
        status=False,
        date_shipped=None)

        # Add members to the order
        self.order.member.add(self.member)

        # Create test order items
        self.order_item = OrderItems.objects.create(
            order=self.order,
            products=self.product,
            price=Money(10.00, 'EUR'),
            quantity=2
        )

        # URLs
        self.order_details_url = reverse('order-details', args=[self.order.id])  # Adjust URL name if different
        self.index_url = reverse('index')  # Adjust URL name if different

    def test_order_details_authenticated_user_valid_order(self):
        """Test order_details view for authenticated user with valid order ID"""
        # Log in the user
        self.client.login(username='testuser', password='testpass123')

        # Make GET request to order_details
        response = self.client.get(self.order_details_url)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order/order_details.html')

        # Check context
        self.assertEqual(response.context['order'], self.order)
        self.assertEqual(list(response.context['items']), [self.order_item])

        # Verify order details
        self.assertEqual(response.context['order'].full_name, 'John Doe')
        self.assertEqual(response.context['items'][0].products.brand, 'TestbrandA')
        self.assertEqual(response.context['items'][0].quantity, 2)

    def test_order_details_authenticated_user_invalid_order(self):
        """Test order_details view for authenticated user with invalid order ID"""
        # Log in the user
        self.client.login(username='testuser', password='testpass123')

        # Make GET request with invalid order ID
        invalid_url = reverse('order-details', args=[999])  # Non-existent order ID
        with self.assertRaises(Order.DoesNotExist):
            self.client.get(invalid_url)
            # Note: If the view handles DoesNotExist (e.g., redirects), adjust the test below

    def test_order_details_unauthenticated_user(self):
        """Test order_details view for unauthenticated user"""
        # Make GET request without logging in
        response = self.client.get(self.order_details_url)

        # Assertions
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index_url)

        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You are not logged in')
        self.assertEqual(messages[0].tags, 'success')


class AdminDashboardTestCase(TestCase):
    def setUp(self):
        # Create a superuser
        self.user = User.objects.create_superuser(
            username="andrejtest",
            password="password123",
            email="andrejtest@example.com"
        )
        # Create a Member instance for the superuser
        self.member = Member.objects.create(user=self.user)

        # Category creation
        self.category = Category.objects.create(name="Category A")

        # Create a test product
        self.product1 = Product.objects.create(
            category=self.category,
            brand="TestbrandA",
            model="Product A",
            price=Money(10.00, 'EUR'),
            image="test.jpg"
        )

        # URLs
        self.payment_info_url = reverse("payment-info")
        self.process_order_url = reverse("process-order")
        self.order_complete_url = reverse("index")

        # Create a test client and log in
        self.client = Client()
        self.client.login(username="andrejtest", password="password123")

        # Manually set up session data
        session = self.client.session
        session['my_shipping'] = {
            'shipping_first_name': 'John',
            'shipping_last_name': 'Doe',
            'shipping_email': 'john.doe@example.com',
            'shipping_address1': '123 Test Street',
            'shipping_address2': '',
            'shipping_city': 'New York',
            'shipping_state': 'NY',
            'shipping_zipcode': '10001',
            'shipping_country': 'USA'
        }

        session['session_key'] = {str(self.product1.id): 2}  # Cart data
        session.save()

        self.order = Order.objects.create(
            # Note: Many-to-many fields (e.g., member) must be added separately after creation
            full_name="John Doe",
            email="john.doe@example.com",
            shipping_label="123 Test Street\n\nNew York\nNY\n10001\nUSA",
            amount_paid=Money(20.00, 'EUR'),
            created_at="2023-10-01 12:00:00",
            status=False,
            date_shipped=None)

        # Add members to the order
        self.order.member.add(self.member)

    def tests_render_order_with_status(self):
        """Test case for rendering and showing up order status as a admin user"""
        super().setUp()

        self.assertEqual(self.order.status, False)
