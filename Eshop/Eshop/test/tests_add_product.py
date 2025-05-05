
from product.form import AddProduct
from django.test import TestCase
from django.urls import reverse
from product.models import Product
from cart.cart import Cart
from product.models import Category
from member.models import Member
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch




class AddProductTest(TestCase):
    def setUp(self):
        # Define valid form data to reuse in each test

        self.category = Category.objects.create(name="Rod")

        # Define valid form data to be reused
        self.valid_form_data = {
            'category': self.category.id,  # Use the ID of the created category
            'brand': 'Hanak',
            'model': 'Superb',
            'price_0': Decimal('1500'),  # MoneyField requires price_0 (value) and price_1 (currency)
            'price_1': 'EUR',
            'image': SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),  # Simulating an empty image, modify with actual `SimpleUploadedFile` if needed
            # 'description': 'No description available.',
        }

    @patch("product.utils.generate_product_description")
    def test_form_valid_data(self, mock_generate_description):
        """ Test case for valid data in the form """
        # Mock the description generator
        mock_generate_description.return_value = "This is a generated description."

        form = AddProduct(data=self.valid_form_data)
        if not form.is_valid():
            print("Form errors:", form.errors)  # Debugging form errors

        self.assertTrue(form.is_valid())  # Ensure that data is valid

        # Save the product and verify it was created
        product = form.save()
        print (product.price.amount)
        self.assertEqual(product, Product.objects.get(brand='Hanak'))
        self.assertEqual(product.model, 'Superb')
        self.assertEqual(product.price.amount, 1500.00)  # Verify the price is saved correctly as Money
        self.assertEqual(product.category, self.category)
        print ("Test case for valid data in the form successfully completed!")


    def test_for_invalid_data(self):
        """ Test case for invalid data in the form"""
        invalid_data = self.valid_form_data.copy()
        invalid_data['price_1'] = 'one hundred' #put text instead of numeric expected input

        form = AddProduct(data=invalid_data) #putting wrong data into the form
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)
        print ("Test case for invalid data in the form successfully completed!")

    def test_for_missing_data(self):
        """ Test case for missing data for the category in the form"""
        missing_data = self.valid_form_data.copy()
        missing_data.pop('category') #taking the category out from data set

        form = AddProduct(data=missing_data) #put missing data into the form
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)
        print ("Test case for missing data in the form successfully completed!")

