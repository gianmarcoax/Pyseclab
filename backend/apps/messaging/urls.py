"""
URLs para messaging app.
"""
from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.list_messages, name='list'),
    path('inbox/', views.inbox, name='inbox'),
    path('sent/', views.sent, name='sent'),
    path('send/', views.send_message, name='send'),
    path('<int:message_id>/', views.get_message, name='detail'),
    path('<int:message_id>/decrypt/', views.decrypt_message, name='decrypt'),
]
