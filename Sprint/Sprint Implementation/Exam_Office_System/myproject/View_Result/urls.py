# view_result/urls.py

from django.urls import path
from . import views

app_name = 'view_result'

urlpatterns = [
    path('', views.ViewResultView.as_view(), name='view_result'),
]
