from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('search/suggestions/', views.search_suggestions, name='search_suggestions'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/<int:pk>/rent/', views.rent_book, name='rent_book'),
    path('book/<int:pk>/purchase/', views.purchase_book, name='purchase_book'),
    path('my-rentals/', views.my_rentals, name='my_rentals'),
    path('my-purchases/', views.my_purchases, name='my_purchases'),
    
    # Административные маршруты
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/users/', views.admin_users, name='admin_users'),
    path('dashboard/users/<int:pk>/', views.admin_user_detail, name='admin_user_detail'),
    path('dashboard/books/', views.admin_books, name='admin_books'),
    path('dashboard/books/add/', views.admin_book_add, name='admin_book_add'),
    path('dashboard/books/<int:pk>/edit/', views.admin_book_edit, name='admin_book_edit'),
    path('dashboard/books/<int:pk>/delete/', views.admin_book_delete, name='admin_book_delete'),
    path('dashboard/rentals/', views.admin_rentals, name='admin_rentals'),
    path('dashboard/rentals/<int:pk>/delete/', views.admin_rental_delete, name='admin_rental_delete'),
    path('dashboard/purchases/', views.admin_purchases, name='admin_purchases'),
    path('dashboard/purchases/<int:pk>/delete/', views.admin_purchase_delete, name='admin_purchase_delete'),
]

