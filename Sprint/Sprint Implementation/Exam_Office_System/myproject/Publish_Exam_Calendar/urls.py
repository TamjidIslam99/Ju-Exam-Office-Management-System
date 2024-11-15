from django.urls import path
from .views import ExamCalendarListView, CreateExamCalendarView, ExamCalendarDetailView

urlpatterns = [
    path('', ExamCalendarListView.as_view(), name='exam_calendar_list'),
    path('create/', CreateExamCalendarView.as_view(), name='create_exam_calendar'),
    path('<int:pk>/', ExamCalendarDetailView.as_view(), name='exam_calendar_detail'),
]
