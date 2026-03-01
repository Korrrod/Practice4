from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='travels/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('travels/', views.travel_list, name='travel_list'),
    path('travels/<int:pk>/', views.travel_detail, name='travel_detail'),
    path('travels/create/', views.travel_create, name='travel_create'),
    path('my-travels/', views.my_travels, name='my_travels'),
]


