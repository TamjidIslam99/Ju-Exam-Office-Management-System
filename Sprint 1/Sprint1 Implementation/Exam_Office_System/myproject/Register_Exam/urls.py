# Register_Exam/urls.py

from django.urls import path
from . import views

app_name = 'register_exam'  # Namespace definition

urlpatterns = [
    path('', views.RegisterExamView.as_view(), name='register_exam'),
    path('confirm/', views.RegisterExamConfirmView.as_view(), name='register_exam_confirm'),
    path('success/', views.RegistrationSuccessView.as_view(), name='registration_success'),
    path('failure/', views.RegistrationFailureView.as_view(), name='registration_failure'),
]
