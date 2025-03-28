from django.urls import path
from . import views


urlpatterns = [
#defining the names for url paths
    path('', views.homepage, name="index" ),
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('about', views.about, name="about"),
    path('category', views.navbar_view, name="category"),
    path('test', views.test, name="test"),

]