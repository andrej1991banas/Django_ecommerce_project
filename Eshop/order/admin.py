from django.contrib import admin
from .models import Order

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'get_member_name')  # Display in admin list

    def get_member_name(self, obj):
        # Access customer's first and last name through the customer relation
        return ", ".join([f"{member.first_name} {member.last_name}" for member in obj.member.all()])

    get_member_name.short_description = 'Customer Name'  # Sets the column name in the admin list view


admin.site.register(Order, OrderAdmin)