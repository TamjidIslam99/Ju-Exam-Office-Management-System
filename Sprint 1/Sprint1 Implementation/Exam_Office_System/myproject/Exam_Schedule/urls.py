from django.urls import path
from .views import CreateExamView

urlpatterns = [
    path('create-exam/', CreateExamView.as_view(), name='create_exam'),
]
