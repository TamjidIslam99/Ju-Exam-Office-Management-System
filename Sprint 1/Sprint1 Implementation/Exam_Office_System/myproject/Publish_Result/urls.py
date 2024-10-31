# Publish_Result/urls.py

from django.urls import path
from .views import SelectExamView, UploadResultsView, SemesterYearlyResultView

app_name = 'publish_result'

urlpatterns = [
    path('select_exam/', SelectExamView.as_view(), name='select_exam'),
    path('upload_results/<int:exam_id>/', UploadResultsView.as_view(), name='upload_results'),
    path('Full/', SemesterYearlyResultView.as_view(), name='semester_yearly_result'),
]
