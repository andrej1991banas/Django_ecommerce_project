from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True, max_length=255, primary_key=True)
    first_name = models.CharField( max_length=255)
    last_name = models.CharField( max_length=255)
    phone_number = models.CharField( max_length=20)
    location = models.CharField( max_length=255)

