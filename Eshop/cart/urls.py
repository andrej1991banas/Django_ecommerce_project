from django.urls import path
from . import views


urlpatterns = [
#defining the names for url paths
    path('cart-summary', views.cart_summary, name="cart-summary"),
    # path('your-name', views.your_name, name="your-name"),
    # path('show-products', views.show_products, name="show-products"),
    # path('product/<int:id>/', views.product_details, name="product-details"),


]