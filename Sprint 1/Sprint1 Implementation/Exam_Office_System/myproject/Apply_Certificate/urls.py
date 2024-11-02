# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('apply_for_certificate/', views.apply_for_certificate, name='apply_for_certificate'),
]
