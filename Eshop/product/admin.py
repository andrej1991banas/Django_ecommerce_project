from django.contrib import admin
from .models import Product, Category

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['category', 'brand', 'model', 'price']  # Display in admin list


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

# Register Member to admin with customization
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
