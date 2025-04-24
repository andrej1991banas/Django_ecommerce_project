from django.db import models
from product.models import Product
from member.models import Member
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime
from djmoney.models.fields import MoneyField


# Define Order model
class Order(models.Model):
    member = models.ManyToManyField(Member, related_name='orders', blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    shipping_label = models.TextField(max_length=1500)
    amount_paid = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR', default = 0)
    created_at = models.DateTimeField(auto_now_add=True) #this is setting now without using datetime module
    status = models.BooleanField(default=False)
    date_shipped = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order {self.pk} created on {self.created_at}'

#Auto Add shipping Date
@receiver (pre_save, sender=Order)
def update_shipping_date(sender, instance, **kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.status and not obj.status:
            instance.date_shipped = now







#define Order Items model
class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    products = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', null=True,)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR', default = 0)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'Order Item {str(self.id)}'




class ShippingAddress (models.Model):
    shipping_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipping_address')
    shipping_first_name = models.CharField(max_length=255)
    shipping_last_name = models.CharField(max_length=255)
    shipping_email = models.EmailField(max_length=255)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255,null=True, blank=True)
    shipping_city = models.CharField(max_length=255)
    shipping_state = models.CharField(max_length=255,null=True, blank=True)
    shipping_zipcode = models.CharField(max_length=255)
    shipping_country = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "shipping address"

    def __str__(self):
        return f'Shipping Address - {str(self.shipping_email)}'

#Create a Shipping Address by default
def create_shipping(sender, instance, created, **kwargs):
    if created:
        user_shipping = ShippingAddress(shipping_user=instance)
        user_shipping.save()
#automate the shipping address creation
post_save.connect(create_shipping, sender=User)