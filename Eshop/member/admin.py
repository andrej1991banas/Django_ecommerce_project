
from django.contrib import admin
from .models import Member



class MemberAdmin(admin.ModelAdmin):
    list_display = ('user','email','first_name','last_name','phone_number','location', 'shipping_address', 'billing_address', 'old_cart')  # Display in admin list
    list_filter = ('user','email','first_name','last_name','location', 'shipping_address', 'billing_address', 'old_cart')  # Filters for easier navigation
    search_fields = ('user','email','first_name', 'last_name')# Allow admin search
    fields = ('user','email','first_name','last_name','phone_number','location', 'shipping_address', 'billing_address', 'old_cart')  # Fields in admin form


# Register Member to admin with customization
admin.site.register(Member, MemberAdmin)