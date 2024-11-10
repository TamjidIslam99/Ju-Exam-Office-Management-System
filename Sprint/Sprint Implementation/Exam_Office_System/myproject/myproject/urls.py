from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accommodation/', include('accommodation_requests.urls')),  # Include the app's URLs
]
