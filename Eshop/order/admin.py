from django.contrib import admin
from .models import Order


# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'get_member_name', 'get_product_order', 'sum_prize')  # Display in admin list

    def get_member_name(self, obj):
        # Access customer's first and last name through the customer relation
        return ", ".join([f"{member.first_name} {member.last_name}" for member in obj.member.all()])

    def get_product_order(self, obj):
        # Access product from order
        return ",".join([f" {product.brand} {product.model}" for product in obj.products.all()])
    def sum_prize(self, obj):
        #access items in order and sum price
        price_get =0
        for price in obj.products.all():
            price_get += price.price
        return ",".join([f" {price_get} "])

    get_member_name.short_description = 'Customer Name'  # Sets the column name in the admin list view
    get_product_order.short_description = 'Product in order'
    sum_prize.short_description = 'Order price'

admin.site.register(Order, OrderAdmin)