# accommodation_requests/urls.py
from django.urls import path
from . import views

app_name = 'accommodation_requests'

urlpatterns = [
    path('request/', views.request_accommodation, name='request_accommodation'),
    path('review/<int:pk>/', views.review_accommodation, name='review_accommodation'),
    path('status/<int:pk>/', views.accommodation_status, name='status'),
]
"""
URL patterns for the accommodation_requests app.

This module defines the URL patterns for the views handling accommodation requests,
reviews by the department, and the status of accommodation requests.

URL Patterns
------------
- request/ : Handles the submission of accommodation requests by students.
- review/<int:pk>/ : Handles the review process by the department for a specific request.
- status/<int:pk>/ : Displays the current status of a specific accommodation request.

Namespaces
----------
app_name : str
    The namespace for these URLs, allowing them to be referenced as 'accommodation_requests:<name>'
    in templates and other areas.
"""
