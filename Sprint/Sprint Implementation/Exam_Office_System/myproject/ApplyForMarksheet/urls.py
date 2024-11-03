# ApplyForMarksheet/urls.py

from django.urls import path
from . import views

app_name = 'apply_marksheet'

urlpatterns = [
    path('apply/', views.apply_marksheet, name='apply_marksheet'),
    path('confirm/', views.confirm_marksheet, name='confirm_marksheet'),
]
