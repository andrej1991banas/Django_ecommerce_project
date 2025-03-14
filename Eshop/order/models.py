from django.db import models
from product.models import Product
from member.models import Member



# Define Order model
class Order(models.Model):
    products = models.ManyToManyField(Product, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True) #this is setting now without using datetime module
    member = models.ManyToManyField(Member, related_name="orders")


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order {self.pk} created on {self.created_at}'
