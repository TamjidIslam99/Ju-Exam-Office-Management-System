# exam_management/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Inventory Management
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/manage/', views.manage_inventory, name='add_inventory'),
    path('inventory/manage/<int:pk>/', views.manage_inventory, name='edit_inventory'),

    # Exam Materials Management
    path('materials/', views.exam_materials_list, name='exam_materials_list'),
    path('materials/add/', views.add_exam_material, name='add_exam_material'),
    path('materials/edit/<int:pk>/', views.edit_exam_material, name='edit_exam_material'),
    path('materials/delete/<int:pk>/', views.delete_exam_material, name='delete_exam_material'),

    # Material Distribution
    path('distribute/', views.distribute_material, name='distribute_material'),
    path('distribution-log/', views.distribution_log, name='distribution_log'),

    # Inventory Alerts
    path('alerts/', views.inventory_alerts, name='inventory_alerts'),
]
