from django.urls import path
from . import views

app_name = 'complaints'

urlpatterns = [
    path('submit/', views.submit_complaint, name='submit_complaint'),
    path('my-complaints/', views.my_complaints, name='my_complaints'),
    path('<int:complaint_id>/', views.complaint_detail, name='complaint_detail'),
]
