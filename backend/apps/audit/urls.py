"""
URLs para audit app.
"""
from django.urls import path
from . import views

app_name = 'audit'

urlpatterns = [
    path('my-activity/', views.my_activity, name='my-activity'),
    path('logs/', views.all_logs, name='all-logs'),
    path('alerts/', views.alerts, name='alerts'),
]
