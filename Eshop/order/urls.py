from django.urls import path
from . import views


urlpatterns = [
#defining the names for url paths
    path('payment-success', views.payment_success, name="payment-success"),
    path('checkout', views.checkout, name="checkout"),
    path('billing-info', views.billing_info, name="billing-info"),
    path('payment-info', views.payment_info, name="payment-info"),
    path('process-order', views.process_order, name="process-order"),
    path('status-shipped', views.status_shipped, name="status-shipped"),
    path('status-not-shipped', views.status_not_shipped, name="status-not-shipped"),
    path ('orders/<int:pk>', views.orders, name="orders"),
    path ('order_details/<int:pk>', views.order_details, name="order-details"),
    ]