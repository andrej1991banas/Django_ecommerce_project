from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
# from django.utils.timezone import now
from order.models import Order
from member.models import Member
import datetime

class StatusNotShippedTestCase(TestCase):
    def setUp(self):
        """
        Set up test data and test client
        """
        # Create superuser (admin)
        self.superuser = User.objects.create_superuser(
            username='admin',
            password='adminpassword',
            email='admin@example.com'
        )

        # Create a regular user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        )

        #Create member
        self.member = Member.objects.create(user=self.user, email=self.user.email, first_name='TestTest')

        # Create test orders
        self.order1 = Order.objects.create(

            status=False,  # Unshipped order
            created_at=datetime.datetime.now(),

        )
        self.order2 = Order.objects.create(

            status=False,  # Unshipped order
            created_at=datetime.datetime.now(),

        )
        self.shipped_order = Order.objects.create(

            status=True,  # Already shipped order
            created_at=datetime.datetime.now(),

        )

        # Set up the client
        self.client = Client()
        self.order1.member.add(self.member)
        self.order2.member.add(self.member)
        self.shipped_order.member.add(self.member)
    def test_superuser_access(self):
        """
        Test that a superuser can access the status_not_shipped endpoint
        """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('status-not-shipped'))
        self.assertEqual(response.status_code, 200)  # Page accessible
        self.assertContains(response, self.order1.id)  # Unshipped order is listed
        self.assertContains(response, self.order2.id)


    def test_regular_user_access_denied(self):
        """
        Test that a regular user cannot access the status_not_shipped endpoint
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('status-not-shipped'))

        self.assertEqual(response.status_code, 302)  # Forbidden for non-superuser
        self.assertRedirects(response,'/')

    def test_unauthenticated_access_denied(self):
        """
        Test that an unauthenticated user cannot access the status_not_shipped endpoint
        """
        response = self.client.get(reverse('status-not-shipped'))
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_unshipped_orders_update(self):
        """
        Test that the status of an unshipped order can be updated by a superuser
        """
        self.client.login(username='admin', password='adminpassword')

        # Send POST request to update status of order1
        response = self.client.post(reverse('status-not-shipped'), {
            'shipping_status': 'True',
            'num': self.order1.id
        })

        # Reload the order from database after update
        self.order1.refresh_from_db()

        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.assertTrue(self.order1.status)  # Status should now be True
        self.assertIsNotNone(self.order1.date_shipped)  # Shipping date should be updated

    # def test_superuser_only_updates_target_order(self):
    #     """
    #     Test that only the target order gets updated
    #     """
    #     self.client.login(username='admin', password='adminpassword')
    #
    #     # Send POST request to update status of order2
    #     response = self.client.post(reverse('status-not-shipped'), {
    #         'shipping_status': 'True',
    #         'num': self.order2.id
    #     })
    #
    #     # Reload both orders from database
    #     self.order1.refresh_from_db()
    #     self.order2.refresh_from_db()
    #
    #     # Assert order statuses
    #     self.assertFalse(self.order1.status)  # Order1 remains unchanged
    #     self.assertTrue(self.order2.status)  # Order2 status updated to True
    #
    #
    #
    # def test_superuser_access_shipped(self):
    #     """
    #     Test that a superuser can access the status_shipped endpoint
    #     """
    #     self.client.login(username='admin', password='adminpassword')
    #     response = self.client.get(reverse('status-shipped'))
    #     self.assertEqual(response.status_code, 200)  # Page accessible
    #     self.assertContains(response, self.shipped_order.id)
    #
    #
    # def test_user_access_shipped(self):
    #     """
    #     Test that a suser cannot access the status_shipped endpoint
    #     """
    #     self.client.login(username='testuser', password='testpassword')
    #     response = self.client.get(reverse('status-shipped'))
    #     self.assertEqual(response.status_code, 302)  # Page accessible
    #     self.assertRedirects(response, '/')

    def test_superuser_access_status_order_page(self):
        """
        Test that a superuser can access the status_order endpoint
        """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(reverse('orders'),  { "shipping_status": "true"})
        # Reload the order from the database
        self.order.refresh_from_db()

        # Assert that the response redirects to 'status-shipped'
        self.assertEqual(response.status_code, 302)  # HTTP 302 (redirect)
        self.assertRedirects(response, reverse("status-shipped"))
