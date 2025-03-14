
from django.contrib import admin
from .models import Member



class MemberAdmin(admin.ModelAdmin):
    list_display = ('user','email','first_name','last_name','phone_number','location')  # Display in admin list
    list_filter = ('location',)  # Filters for easier navigation
    search_fields = ('first_name', 'last_name')# Allow admin search
    fields = ('user','email','first_name','last_name','phone_number','location')  # Fields in admin form


# Register Member to admin with customization
admin.site.register(Member, MemberAdmin)