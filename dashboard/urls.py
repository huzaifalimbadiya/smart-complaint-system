from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('complaints/', views.manage_complaints, name='manage_complaints'),
    path('complaints/<int:complaint_id>/update/', views.update_complaint, name='update_complaint'),
    path('reports/excel/', views.export_excel, name='export_excel'),
    path('reports/pdf/', views.export_pdf, name='export_pdf'),
]
