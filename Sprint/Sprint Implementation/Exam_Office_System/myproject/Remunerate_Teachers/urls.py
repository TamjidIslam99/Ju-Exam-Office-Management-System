# Remunerate_Teachers/urls.py

from django.urls import path
from .views import (
    CreateRemunerationsView,
    RemunerationsListView,
    PendingRemunerationsView,
    UpdateRemunerationStatusView,
)

app_name = 'remunerate_teachers'

urlpatterns = [
    path('create/', CreateRemunerationsView.as_view(), name='create_remunerations'),
    path('list/', RemunerationsListView.as_view(), name='remunerations_list'),
    path('pending/', PendingRemunerationsView.as_view(), name='pending_remunerations'),
    path('update-status/', UpdateRemunerationStatusView.as_view(), name='update_remuneration_status'),
]
