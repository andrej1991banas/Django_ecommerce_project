from django.contrib import admin


from .models import Order, ShippingAddress, OrderItems


# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'full_name', 'shipping_label', 'amount_paid', 'status', 'date_shipped')  # Display in admin list

class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'products', 'quantity', 'price')  # Display in admin list


admin.site.register(Order, OrderAdmin)
admin.site.register(ShippingAddress)
admin.site.register(OrderItems,OrderItemsAdmin)


class OrderItemsInline(admin.StackedInline):
    model = OrderItems
    extra = 0


#Extend Order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly = ('created_at',)
    inlines = [OrderItemsInline]
    list_display = ('id', 'created_at', 'full_name', 'shipping_label', 'amount_paid', 'status', 'date_shipped')  # Display in admin list

#unregister Order model
admin.site.unregister(Order)

#Re-Register Order and OrderAdmin
admin.site.register(Order, OrderAdmin)