"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('Authentication.urls')),
    path('attend/', include('TrackingAttendence.urls')),
    path('marksheet/', include('ApplyForMarksheet.urls')),

    path('publish_result/', include('Publish_Result.urls')),
    path('answer_scripts/', include('Answer_Script_Management.urls')),

    path('materials/', include('Manage_Exam_Materials.urls')),
    path('publish_result/', include('Publish_Result.urls')),
    path('register-exam/', include('Register_Exam.urls')),

    path('remunerate/', include('Remunerate_Teachers.urls')),
    path('view_result/', include('View_Result.urls')),
]
