import os
import django

# Explicitly set the DJANGO_SETTINGS_MODULE variable at runtime if not set
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eshop.settings")
django.setup()


from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from product.models import Category, Product
from member.models import Member





@override_settings(ALLOWED_HOSTS=['testserver'])
class CrudUserTestCase(TestCase):
    def setUp(self):
        """Setup pre-test data for the test case"""
        #Create User for Member
        self.user = User.objects.create(username= "andrejtest", first_name="Testandrej", last_name="Test", email="andrej@test.com")


    def test_user_creation(self):
        """Test if the model object is being created correctly."""
        self.assertEqual(self.user.username, "andrejtest")
        self.assertEqual(self.user.last_name, "Test")
        self.assertIsNotNone(self.user.id)


    def test_user_str_method(self):
        """ Test if the model User is being printed correctly."""
        self.assertEqual(str(self.user), "andrejtest")


    def test_user_update_method(self):
        """ Test if the User model is being updated correctly."""
        self.user.first_name = "Testandrej2"
        self.user.save()

        user= User.objects.get(id=self.user.id)

        self.assertEqual(user.first_name, "Testandrej2") #check updated data
        self.assertEqual(user.last_name, "Test") #check not updated data


    def test_user_delete_method(self):
        """ Test if the User model is being deleted correctly."""
        self.user.delete()

        self.assertFalse(User.objects.filter(id=self.user.id).exists())


class CrudMemberTestCase(TestCase):
    def setUp(self):
        """Setup pre-test data for the test case"""
        # Create User for Member
        self.user = User.objects.create(username="andrejtest", first_name="Testandrej", last_name="Test",
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


    def test_member_creation(self):
        """ Test if the member object is being created correctly. """
        self.assertEqual(self.member.user.first_name, "Testandrej") #User model tangled with Member model with user and OneToOne field
        self.assertEqual(self.member.user.email, "andrej@test.com") #User model tangled with Member model with user and OneToOne field
        self.assertIsNotNone(self.member.user.id) #User model tangled with Member model with user and OneToOne field
        self.assertEqual(self.member.gender, "Male") #actual Member data
        self.assertEqual(self.member.city, "TestCity") #actual Member data

    def test_member_str_method(self):
        """ Test if the Member model is being printed correctly. """
        self.assertEqual(str(self.member),"Testandrej Test (andrej@test.com)" )


    def test_member_update_method(self):
        """ Test if the Member model is being updated correctly. """
        self.member.first_name = "Testandrej2"
        self.member.save()

        member= Member.objects.get(gender="Male")

        self.assertEqual(member.first_name, "Testandrej2")#test updated data
        self.assertEqual(member.last_name, "Test") #test old data
        self.assertEqual(member.user.email, "andrej@test.com")


    def test_member_delete_method(self):
        """ Test if the model Member is  being deleted correctly."""
        member = Member.objects.get(phone_number="123456789")
        member.delete() #delete the Member

        self.assertFalse(Member.objects.filter(first_name="Testandrej").exists()) #check if the querry of Members is empty




class CrudProductTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.category_rods = Category.objects.create(id=1, name="Rods")

        # Create dummy products for the category
        self.prod=Product.objects.create(model="Fly Rod A",brand="Hanak", category=self.category_rods, price=100.00)


    def test_create_category_method(self):
        """" TEst if the model Category is being created correctly"""
        self.assertEqual(self.category_rods.name, "Rods")
        self.assertIsNotNone(self.category_rods.id)


    def test_read_category_method(self):
        """ Test if the model Category is being read correctly"""
        self.assertEqual(str(self.category_rods), "Rods")


    def test_update_category_method(self):
        """ Test if the model Category is being updated correctly"""
        self.category_rods.name="Rods2"
        self.category_rods.save()
        self.assertEqual(self.category_rods.name, "Rods2") #test updated data


    def test_delete_category_method(self):
        """Test if the model Category is being deleted correctly"""
        self.category_rods.delete() #delete category
        self.assertFalse(Category.objects.filter(id=1).exists()) #verify its does not exist


    def test_create_product_method(self):
        """" Test if the model Product is being created correctly"""

        self.assertEqual(self.prod.model, "Fly Rod A")
        self.assertEqual(self.prod.price.amount, 100.00)
        self.assertEqual(self.prod.category.name, "Rods")


    def test_read_product_method(self):
        """ Test if the model Product is being read correctly"""
        self.assertEqual(str(self.prod), "Hanak Fly Rod A")


    def test_update_product_method(self):
        """ Test if the model Product is being updated correctly"""
        prod = Product.objects.get(model="Fly Rod A")
        prod.price = 150.00
        prod.save()
        self.assertEqual(prod.price.amount, 150.00)
        self.assertEqual(prod.model, "Fly Rod A")


    def test_delete_product_method(self):
        """ Test if the model Product is being deleted correctly"""
        self.prod.delete()
        self.assertFalse(Product.objects.filter(model="Fly Rod A").exists())





