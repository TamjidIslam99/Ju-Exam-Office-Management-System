from django.urls import path
from . import views

urlpatterns = [
    path('select_exam/', views.select_exam, name='select_exam'),
    path('input_result/<int:exam_id>/', views.input_result, name='input_result'),
    path('review_results/<int:exam_id>/', views.review_results, name='review_results'),
    path('publish_results/<int:exam_id>/', views.publish_results, name='publish_results'),
]
