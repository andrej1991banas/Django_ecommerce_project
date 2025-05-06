import os
import django

# Explicitly set the DJANGO_SETTINGS_MODULE variable at runtime if not set
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eshop.settings")
django.setup()

from django.test import TestCase, override_settings, RequestFactory
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from product.models import Category, Product
from member.models import Member
from cart.cart import Cart
from django.contrib.sessions.backends.db import SessionStore





class MyViewTestCase(TestCase):
    def test_homepage(self):
        """Test if the homepage returns a 200 HTTP status."""
        response = self.client.get(reverse("index"))  # Use reverse() for named URL patterns
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Thymallus Flyfishing")  # Check content
        print ("Test case for loading homepage successfully finished")


    def test_about(self):
        """Test if the about returns a 200 HTTP status."""
        response = self.client.get(reverse("about"))  # Use reverse() for named URL patterns
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "About Us ...")  # Check content
        print("Test case for loading about successfully finished")


    def test_register(self):
        """Test if the register returns a 200 HTTP status."""
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Register")  # Check content
        print("Test case for loading register page successfully finished")


    def test_login(self):
        """Test if the login returns a 200 HTTP status."""
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign In")  # Check content
        print("Test case for loading login page successfully finished")


    def test_navbar(self):
        """Test if the navbar page showing the search of products by category."""
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Rod")
        self.assertContains(response, "Reels")
        self.assertContains(response, "Fly Lines")

        #ensuring that navbar downdrop showing all categories from products
        print("Test case for loading navbar and its items successfully finished")


    def test_cart_summary(self):
        """Test if the cart summary page showing the  products in the cart."""
        response = self.client.get(reverse("cart-summary"))
        self.assertEqual(response.status_code, 200)     #check what is on the cart summary page
        self.assertContains(response, "Shopping cart")
        self.assertContains(response, "Now check your cart")
        print("Test case for loading cart summary page successfully finished")



class LoginRequiredPages(TestCase):
    """ Test pages for login required message"""
    def test_update_password(self):
        """Test if the update password page returns an error message if not logged in."""
        response = self.client.get(reverse("update-password"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))  # Ensure the expected redirection

        response = self.client.get(reverse("update-password"), follow=True)
        self.assertEqual(response.status_code, 200)

        # Follow the redirection and check for messages
        messages = list(get_messages(response.wsgi_request))

        # Assert messages exist
        self.assertTrue(len(messages) > 0)  # This will clarify why the test fails
        self.assertEqual(str(messages[0]), "You must be logged in to access this page")  # Check the exact message
        print("Test case for non authenticated user trying to access update password page successfully finished")


    def test_update_user(self):
        """Test if the update user page returns an error message if not logged in."""
        response = self.client.get(reverse("update"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))  # Ensure the expected redirection

        response = self.client.get(reverse("update"), follow=True)
        self.assertEqual(response.status_code, 200)

        # Follow the redirection and check for messages
        messages = list(get_messages(response.wsgi_request))

        # Assert messages exist
        self.assertTrue(len(messages) > 0)  # This will clarify why the test fails
        self.assertEqual(str(messages[0]), "You must be logged in to access this page")  # Check the exact message
        print("Test case for non authenticated user trying to access update user details page successfully finished")


    def test_dashboard(self):
        """ Test if the dashboard page returns an error message if not logged in."""
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))  # Ensure the expected redirection

        response = self.client.get(reverse("dashboard"), follow=True)
        self.assertEqual(response.status_code, 200)

        # Follow the redirection and check for messages
        messages = list(get_messages(response.wsgi_request))

        # Assert messages exist
        self.assertTrue(len(messages) > 0)  # This will clarify why the test fails
        self.assertEqual(str(messages[0]), "You must be logged in to access this page")  # Check the exact message
        print("Test case for non authenticated user trying to access dashboard page successfully finished")


    def test_add_product(self):
        """ Test if the add product page loads successfully"""
        response = self.client.get(reverse("add-product"))
        self.assertEqual(response.status_code, 200)  # check what is on the cart summary page
        self.assertContains(response, "Add Product") # check the successful loading og the page
        print("Test case for loading add product page successfully finished")


    def test_checkoout(self):
        """ Test if the checkout page loads successfully"""
        response = self.client.get(reverse("checkout"))
        self.assertEqual(response.status_code, 200)     #check what is on the checkout page
        self.assertContains(response, "Shopping cart")
        print("Test case for loading checkout page successfully finished")


    def test_billing_info(self):
        """ Test if the billing info page loads successfully"""
        response = self.client.get(reverse("billing-info"))
        self.assertEqual(response.status_code, 302)     #check what is on the billing info page
        self.assertRedirects(response, reverse("index"))
        print("Test case for loading billing info page successfully finished")



class CategorySearchTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.category_rods = Category.objects.create(id=1, name="Rods")
        self.category_reels = Category.objects.create(id=2, name="Reels")
        self.category_fly_line = Category.objects.create(id=3, name="Fly Lines")
        self.category_nets = Category.objects.create(id=4, name="Nets")

        # Create dummy products for the category
        Product.objects.create(model="Fly Rod A", category=self.category_rods, price=100.00)
        Product.objects.create(model="Fly Rod B", category=self.category_rods, price=200.00)
        Product.objects.create(model="Fly Rod C", category=self.category_rods, price=300.00)
        Product.objects.create(model="Reel A", category=self.category_reels, price=80.00)
        Product.objects.create(model="Reel B", category=self.category_reels, price=100.00)
        Product.objects.create(model="Reel C", category=self.category_reels, price=120.00)
        Product.objects.create(model="Fly Line A", category=self.category_fly_line, price=80.00)
        Product.objects.create(model="Fly Line B", category=self.category_fly_line, price=90.00)
        print("Created test products")


    def test_category_search(self):
        """ Test if clicking on the link in dropdown menu redirects to the correct page.
        With correct content or products from that category"""

        category_id = 1  # Example: Switch to "Rods"
        url = reverse('category-search', args=[category_id])

        #Make a GET request to this URL
        response = self.client.get(url)

        #assert response status for this page
        self.assertEqual(response.status_code, 200)
        #assert using of right template
        self.assertTemplateUsed(response, 'product/category_search.html')
        #check if the page rendering the right data
        self.assertContains( response, 'Rods') #check rendering page with "rod" category
        self.assertContains(response, 'Fly Rod A')
        self.assertContains(response, 'Fly Rod B')
        self.assertNotContains(response, 'Fly line A') #check for rendering the wrong data
        self.assertNotContains(response, 'Reel A')
        print("Search by category id=1 successfully finished")

        #check for category of Reels
        category_id = 2  # Example: Switch to "Reels"
        url = reverse('category-search', args=[category_id])

        # assert response status for this page
        self.assertEqual(response.status_code, 200)
        # Make a GET request to this URL
        response = self.client.get(url)
        self.assertContains(response, 'Reels')  # check rendering page with "reel" category
        self.assertContains(response, 'Reel A')
        self.assertContains(response, 'Reel C')
        self.assertNotContains(response, 'Fly line B')  # check for rendering the wrong data
        self.assertNotContains(response, 'Fly Rod A')
        print("Search by category id=2 successfully finished")

        # check for category of Fly Lines
        category_id = 3  # Example: Switch to "Fly Lines"
        url = reverse('category-search', args=[category_id])

        # assert response status for this page
        self.assertEqual(response.status_code, 200)
        # Make a GET request to this URL
        response = self.client.get(url)
        self.assertContains(response, 'Fly Lines')  # check rendering page with "reel" category
        self.assertContains(response, 'Fly Line A')
        self.assertContains(response, 'Fly Line B')
        self.assertNotContains(response, 'Reel B')  # check for rendering the wrong data
        self.assertNotContains(response, 'Fly Rod A')
        print("Search by category id=3 successfully finished")

        category_id = 4  # Example: Switch to "Nets" which does not contain any products
        url = reverse('category-search', args=[category_id])

        # Make a GET request to this URL
        response = self.client.get(url)

        # assert response status for this page
        self.assertEqual(response.status_code, 200)
        # assert using of right template
        self.assertTemplateUsed(response, 'product/category_search.html')
        # but rendering the empty page, not 404 page
        self.assertContains(response, "No products available in this category.")
        print("Search by category id=4 successfully finished")

        #check the 404 not found page
        category_id = 5
        url = reverse('category-search', args=[category_id])

        # Make a GET request to this URL
        response = self.client.get(url)
        #check for 404 not found status page if we use ID for non existing category of product
        self.assertEqual(response.status_code, 404)
        print("Search by category id=5 successfully finished")

    def tests_category_summary_page(self):
        """ Test case for rendering category search with page containing oll categories"""
        categories = Category.objects.all()
        url = reverse('category-summary')
        # Make a GET request to this URL
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rods')
        print ("Test case for category summary page was successful!")

    def tests_404_page(self):
        """ Test case for rendering 404 error page"""

        # Make a GET request to this URL
        response = self.client.get('/non-existent-page/')

        # Verify the response status
        self.assertEqual(response.status_code, 404)  # Status code for "Not Found"

        # Optional: Verify the correct template is used
        # Assuming you have a 404.html template configured in your settings
        self.assertTemplateUsed(response, 'product/404.html')
        print("404 error page test completed successfully!")




class ProductDetailsTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.category_rods = Category.objects.create(id=1, name="Rods")
        self.category_reels = Category.objects.create(id=2, name="Reels")
        self.category_fly_line = Category.objects.create(id=3, name="Fly Lines")
        self.category_nets = Category.objects.create(id=4, name="Nets")

        # Create dummy products for the category
        Product.objects.create(id=1, model="Fly Rod A", brand="Hanak Test Rod", category=self.category_rods, price=110.00, image= None)
        Product.objects.create(id=2, model="Fly Rod B",brand="Hardy Test Rod", category=self.category_rods, price=200.00)
        Product.objects.create(id=4, model="Reel A", brand="Hanak Test Reel", category=self.category_reels, price=80.00)
        Product.objects.create(id=5, model="Reel B",brand="Hardy Test Reel", category=self.category_reels, price=100.00)
        Product.objects.create(id=7, model="Fly Line A",brand="Hanak Test Line", category=self.category_fly_line, price=70.00)
        Product.objects.create(id=8, model="Fly Line B", brand="Hardy Test Line", category=self.category_fly_line, price=90.00)
        print("Test products created")


    def test_product_details(self):
        """" testing rendering pages with product details according to their ids"""

        #set for the details of the first product
        id = 1
        url = reverse('product-details', args=[id])

        #Make a GET request to this URL
        response = self.client.get(url)

        #check details for the first product
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fly Rod A')
        self.assertContains(response, 'Hanak Test')
        self.assertNotContains(response, 'Fly Rod B')#checks for wrong data
        self.assertNotContains(response, 'Hardy Test Line')
        print("Test product details for product id=1 was successful!")

        #set for the details of the first product
        id = 7
        url = reverse('product-details', args=[id])

        # Make a GET request to this URL
        response = self.client.get(url)

        # check details for the first product
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fly Line A')
        self.assertContains(response, '70.00')
        self.assertNotContains(response, 'Fly Rod A')  # checks for wrong data
        self.assertNotContains(response, 'Hardy Test Line')
        print("Test product details for product id=7 was successful!")




class CartTestCase(TestCase):
    def setUp(self):
        """Setup test environment."""
        # Create a user and member
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.member = Member.objects.create(user=self.user, old_cart="")

        #Create test product
        self.category_rods = Category.objects.create(id=1, name="Rods")
        self.category_reels = Category.objects.create(id=2, name="Reels")
        self.category_fly_line = Category.objects.create(id=3, name="Fly Lines")
        self.category_nets = Category.objects.create(id=4, name="Nets")

        # Create dummy products for the category
        self.product_1=Product.objects.create(id=1, model="Fly Rod A", brand="Hanak Test Rod", category=self.category_rods, price=110.00, image= None)
        self.product_2=Product.objects.create(id=2, model="Fly Rod B",brand="Hardy Test Rod", category=self.category_rods, price=200.00)
        self.product_3=Product.objects.create(id=3, model="Reel A", brand="Hanak Test Reel", category=self.category_reels, price=80.00)
        self.product_4=Product.objects.create(id=4, model="Reel B",brand="Hardy Test Reel", category=self.category_reels, price=100.00)
        self.product_5=Product.objects.create(id=5, model="Fly Line A",brand="Hanak Test Line", category=self.category_fly_line, price=70.00)
        self.product_6=Product.objects.create(id=6, model="Fly Line B", brand="Hardy Test Line", category=self.category_fly_line, price=90.00)

        # Create a mock request
        self.factory = RequestFactory()
        self.cart_url = reverse('cart-summary')
        self.request = self.factory.get("/")
        self.request.user = self.user
        self.request.session = SessionStore()
        self.cart = Cart(self.request)  # Create an instance of the Cart class


    def test_cart_initialization(self):
        """ test that the cart initializes correctly"""
        self.assertEqual(len(self.cart), 0) #asume empty cart
        self.assertIsInstance(self.cart.cart, dict) #check the cart is dictionary {'price': str(product.price)}
        self.assertTrue('session_key' in self.request.session)  # Ensure the session key is set
        print("Test case for initialization of an empty cart was successful!")


    def test_add_product_to_cart(self):
        """Test adding a product to the cart."""
        self.cart.add(self.product_1.id,1)  # Add product to the cart
        products = list(self.cart.get_cart_prods())
        self.assertIn(str(self.product_1.id), self.cart.cart)  # Verify product is in the cart
        self.assertEqual(len(self.cart), 1)  # Verify cart size is now 1
        self.assertIn(self.product_1, products)  # Ensure product1 is in the fetched list
        print("Test case for adding item to the cart was successful!")


    def test_get_cart_products(self):
        """Test fetching products from the cart."""
        self.cart.add(self.product_4.id,2)  # Add products to cart
        self.cart.add(self.product_2.id,1)
        products = list(self.cart.get_cart_prods())
        self.assertEqual(len(products), 2)  # Verify 2 products are fetched
        self.assertIn(self.product_4, products)  # Ensure product1 is in the fetched list
        self.assertIn(self.product_2, products)  # Ensure product2 is in the fetched list
        print("Test case for getting items  from the cart was successful!")


    def test_cart_total(self):
        """Test the cart total calculation."""
        self.cart.add(self.product_1.id, 2)  # Add products to cart

        self.cart.add(self.product_2.id, 3)
        total = self.cart.cart_total()  # Calculate total
        self.assertEqual(total.amount, 820)  # Verify total calculation for price is correct
        print("Test case cart total was successful!")


    def test_empty_cart(self):
        """Test an empty cart returns correct total and product list. And showing the message."""
        self.assertEqual(self.cart.cart_total(), 0)  # Total should be 0
        self.assertEqual(len(self.cart.get_cart_prods()), 0)  # No products should be returned

        # Mock an authenticated request
        request = self.factory.get(self.cart_url)
        request.user = self.user
        request.session = {}  # Mock an empty session

        # Simulate visiting the cart view (replace `cart_view` with your actual cart view)
        response = self.client.get(self.cart_url)

        # Assert that the "No products in your shopping cart" message is rendered
        self.assertContains(response, "No products in your shopping cart")
        self.assertEqual(response.status_code, 200)
        print("Test case for empty cart after deletion was successful!")

