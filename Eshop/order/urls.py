from django.urls import path
from . import views


urlpatterns = [
#defining the names for url paths
    path('payment-success', views.payment_success, name="payment-success"),
    path('checkout', views.checkout, name="checkout"),
    ]