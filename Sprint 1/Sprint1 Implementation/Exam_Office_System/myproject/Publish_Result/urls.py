# Publish_Result/urls.py

from django.urls import path
from .views import SelectExamView, UploadResultsView

app_name = 'publish_result'

urlpatterns = [
    path('select_exam/', SelectExamView.as_view(), name='select_exam'),
    path('upload_results/<int:exam_id>/', UploadResultsView.as_view(), name='upload_results'),
]
