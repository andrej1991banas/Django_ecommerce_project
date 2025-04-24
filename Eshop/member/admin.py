
from django.contrib import admin
from .models import Member
from django.contrib.auth.models import User



class MemberAdmin(admin.ModelAdmin):
    list_display = ('user','email','first_name','last_name','phone_number','gender', 'country', 'old_cart')  # Display in admin list
    list_filter = ('user','email','first_name','last_name','phone_number','gender', 'country', 'old_cart')  # Filters for easier navigation
    search_fields = ('user','email','first_name', 'last_name')# Allow admin search
    fields = ('user','email','first_name','last_name','phone_number','gender', 'country', 'old_cart')  # Fields in admin form

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','email','first_name','last_name','is_staff')

# Register Member to admin with customization
admin.site.register(Member, MemberAdmin)


class MemberInline(admin.StackedInline):
    model = Member
    extra = 0


#Extend User model
class UserAdmin(admin.ModelAdmin):
    model = User
    inlines = [MemberInline]

#unregister User model
admin.site.unregister(User)

#Re-Register User and UserAdmin
admin.site.register(User,UserAdmin)