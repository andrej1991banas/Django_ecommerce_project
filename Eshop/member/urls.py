from django.urls import path
from . import views


urlpatterns = [
#defining the names for url paths
    path('', views.homepage, name="index" ),
    path('register', views.register, name="register"),
    path('update', views.update_user, name="update"),
    path('update-password', views.update_password, name="update-password"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('about', views.about, name="about"),
    path('category', views.navbar_view, name="category"),
    path('test', views.test, name="test"),
    path('search', views.search, name="search"),

]