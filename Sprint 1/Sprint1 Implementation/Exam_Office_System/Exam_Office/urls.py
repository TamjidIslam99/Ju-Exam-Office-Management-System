# appname/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Define routes and associate them with views
]
