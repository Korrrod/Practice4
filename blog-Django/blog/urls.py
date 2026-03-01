from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from . import views
from .forms import CustomAuthenticationForm

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html', authentication_form=CustomAuthenticationForm), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.public_posts, name='public_posts'),
    path('feed/', views.feed, name='feed'),
    path('my-blog/', views.my_blog, name='my_blog'),
    path('post/new/', views.create_post, name='create_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:pk>/request-access/', views.request_access, name='request_access'),
    path('access-request/<int:pk>/<str:action>/', views.handle_access_request, name='handle_access_request'),
    path('u/<str:username>/', views.user_profile, name='user_profile'),
    path('u/<str:username>/follow/', views.toggle_follow, name='toggle_follow'),
    re_path(r'^tags/(?P<slug>[^/]+)/$', views.posts_by_tag, name='posts_by_tag'),
]


