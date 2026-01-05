"""
URLs para crypto_core app.
"""
from django.urls import path
from . import views

app_name = 'crypto_core'

urlpatterns = [
    # Generación de claves
    path('keys/generate/', views.generate_keys, name='generate-keys'),
    
    # AES
    path('aes/encrypt/', views.aes_encrypt, name='aes-encrypt'),
    path('aes/decrypt/', views.aes_decrypt, name='aes-decrypt'),
    
    # RSA
    path('rsa/encrypt/', views.rsa_encrypt, name='rsa-encrypt'),
    path('rsa/decrypt/', views.rsa_decrypt, name='rsa-decrypt'),
    path('rsa/sign/', views.rsa_sign, name='rsa-sign'),
    path('rsa/verify/', views.rsa_verify, name='rsa-verify'),
]
