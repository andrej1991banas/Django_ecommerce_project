from django.urls import path
from . import views


urlpatterns = [
#defining the names for url paths
    path('add-product', views.add_product, name="add-product"),
    path('show-products', views.show_products, name="show-products"),
    path('product/<int:id>/', views.product_details, name="product-details"),
    path ('category/<int:category_id>/', views.category_rods, name="category-search"),
]