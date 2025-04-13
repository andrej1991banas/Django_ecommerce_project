from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="member")
    email = models.EmailField(unique=True, max_length=255, primary_key=True)
    first_name = models.CharField( max_length=255)
    last_name = models.CharField( max_length=255)
    phone_number = models.CharField( max_length=20)
    address1 = models.CharField( max_length=255)
    address2 = models.CharField( max_length=255, blank=True, null=True)
    city = models.CharField( max_length=255)
    state = models.CharField( max_length=255, blank=True, null=True)
    zipcode = models.CharField( max_length=255)
    country = models.CharField( max_length=255)
    old_cart = models.CharField( max_length=255, blank=True, null=True)

    def __str__(self):
        return self.email

