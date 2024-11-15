from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect  # Only one import is needed
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('Authentication.urls')),  # Authentication app URLs
    path('calendar/', include('Publish_Exam_Calendar.urls')),  # Publish_Exam_Calendar app URLs
    # You can add more paths as needed for other apps
]
