from django.urls import path
from . import views


urlpatterns = [
#defining the names for url paths
    path('cart', views.cart_summary, name="cart-summary"),
    path('add/', views.cart_add, name="cart-add"),
    path('update/', views.cart_update, name="cart-update"),
    path('delete/', views.cart_delete, name="cart-delete"),
]