from django.test import TestCase
from django.urls import reverse
from product.models import Product
from cart.cart import Cart
from order.models import Order
from product.models import Category


class EcommerceTestCase(TestCase):
    def setUp(self):
        """Set up initial data for testing"""
        #category creation
        self.category = Category.objects.create(name="Category A")
        # Create products
        self.product1 = Product.objects.create(category=self.category,brand="TestbrandA", model="Product A", price=10.0 )
        self.product2 = Product.objects.create(category=self.category, brand="TestbrandB",model="Product B", price=20.0)
        self.cart_add_url = reverse("cart-add")


    # def test_render_products(self):
    #     """ Test case for rendering the page with products"""
    #     # Test to ensure products can be viewed
    #     response = self.client.get(reverse("show-products"))  # Define your product list URL
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, self.product1.model)
    #     self.assertContains(response, self.product2.model)
    #     print("Test case for rendering the page with products successfully completed!")
    #
    #
    # def test_add_to_cart(self):
    #     """ Test case for adding a product to the cart."""
    #     # Simulate adding a product to the cart
    #     response = self.client.post(self.cart_add_url, {
    #         'action': 'post',
    #         'product_id': self.product1.id,  # Set product ID
    #         'product_qty': 2,  # Set quantity
    #     })
    #
    #     # Check the JSON response for cart quantity
    #     self.assertIn("qty", response.json())
    #     self.assertEqual(response.json()["qty"], 1)  # Ensure quantity matches
    #     print(" Successfully added product to the cart and updated number of items inside the cart")
    #
    #     # Verify the cart contents (from session) and verify it is not empty
    #     cart= Cart(self.client) #getting cart instance
    #     self.assertTrue(cart.__len__() > 0)
    #     cart_products = cart.get_cart_prods()
    #     self.assertEqual(len(cart_products), 1)
    #     print ("Cart has one item in it.")
    #
    #     cart_content = list(cart.cart.items())
    #     self.assertEqual(cart_content[0] , (str(self.product1.id),2))
    #
    #     # Check the product and quantity in the cart
    #     cart_items = list(cart.cart.values())  # Retrieve the items in the cart
    #     self.assertEqual(len(cart_items), 1)  # Ensure there is only one item in the cart
    #     self.assertEqual(cart_items[0], 2)  # Match product quantity
    #     print ("Cart instance returning dict with id of the product and quantity.")
    #
    #     print ("Test case for adding a product to the cart successfully completed!")


    # def test_update_cart_check_total(self):
    #     """ Test case for updating the cart quantities and checking the total price."""
    #     # Add to cart first
    #     response = self.client.post(self.cart_add_url, {
    #                 'action': 'post',
    #                 'product_id': self.product1.id,  # Set product ID
    #                 'product_qty': 2,  # Set quantity
    #             })
    #
    #     cart = Cart(self.client)  # getting cart instance
    #     cart_qty = list(cart.cart.values())[0]
    #     self.assertEqual(cart_qty, 2)
    #     print ("Cart has quantity of 2 items in it.")
    #
    #     # Update the cart quantity
    #     response = self.client.post(reverse("cart-update"), {
    #                 'action': 'post',
    #                 "product_id": self.product1.id,
    #                 "product_qty": 5
    #             })
    #     # Check the JSON response for cart quantity
    #     self.assertIn("quantity", response.json())
    #
    #     # # Verify the updated quantity
    #     cart= Cart(self.client) #getting cart instance
    #     cart_qty = list(cart.cart.values())[0]
    #     self.assertEqual (cart_qty,5)
    #     print("Cart has updated quantity of 5 items in it.")
    #
    #     totals = cart.cart_total() #call the cart_total to get total price of the cart
    #     self.assertEqual(totals.amount, 50.00) #total count as qty*price
    #     print ("Test case for updating the cart quantities and checking the total price successfully completed!")


    # def test_delete_cart(self):
    #     """ Test case for updating the cart quantities and checking the total price."""
    #     # Add to cart first
    #     self.client.post(self.cart_add_url, {
    #                 'action': 'post',
    #                 'product_id': self.product1.id,  # Set product ID
    #                 'product_qty': 2,  # Set quantity
    #             })
    #
    #     self.client.post(self.cart_add_url, {
    #         'action': 'post',
    #         'product_id': self.product2.id,  # Set product ID
    #         'product_qty': 3,  # Set quantity
    #     })
    #
    #
    #     self.assertEqual
    #     cart = Cart(self.client)  # getting cart instance
    #
    #     self.assertTrue(cart.__len__() == 2) #the products is in the cart
    #     print ("Cart has 2 items in it.")
    #
    #     # Delete item from the cart
    #     response = self.client.post(reverse("cart-delete"), {
    #                 'action': 'post',
    #                 "product_id": self.product1.id
    #             })
    #     self.assertNotIn(self.product1.id, response.json())
    #     print ("Product 1 was deleted from the cart.")
    #     print (" Test case for deleting the cart item successfully completed!")


    def test_checkout(self):
        """ Test case for checkout process."""
        # Add to cart first
        self.client.post(self.cart_add_url, {
                    'action': 'post',
                    'product_id': self.product1.id,  # Set product ID
                    'product_qty': 2,  # Set quantity
                })

        # Proceed to checkout
        response = self.client.post(reverse("checkout"))
        self.assertEqual(response.status_code, 200)

        # # Verify the order is created
        # order = Order.objects.get(user=self.client)
        # self.assertEqual(order.items.count(), 1)
        # self.assertEqual(order.total_price, self.product2.price)
    #
    # def test_payment_processing(self):
    #     # Add product to cart and checkout
    #     self.client.post(reverse("add_to_cart"), {"product_id": self.product1.id, "quantity": 3})
    #     self.client.post(reverse("checkout"))
    #
    #     # Simulate payment processing
    #     response = self.client.post(reverse("process_payment"), {"order_id": 1, "payment_method": "credit_card"})
    #     self.assertEqual(response.status_code, 200)
    #
    #     # Verify payment is completed
    #     order = Order.objects.get(user=self.client)
    #     self.assertTrue(order.is_paid)
