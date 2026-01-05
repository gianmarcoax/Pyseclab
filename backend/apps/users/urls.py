"""
URLs para users app.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = 'users'

urlpatterns = [
    # Auth
    path('register/', views.register, name='register'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # Current user
    path('me/', views.me, name='me'),
    path('me/keys/', views.my_keys, name='my-keys'),
    path('me/keys/generate/', views.generate_my_keys, name='generate-my-keys'),
    
    # Other users
    path('users/', views.list_users, name='list-users'),
    path('users/public-key/', views.get_public_key, name='get-public-key'),
]
