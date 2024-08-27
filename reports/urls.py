from django.urls import path
from . import views

urlpatterns = [
    path('generate_excel_report', views.generate_excel_report, name='generate_excel_report'),
    path('Generated_Reports/<str:filename>/', views.serve_report, name='serve_report'),
    path('generated_reports', views.generated_reports, name='generated_reports'),
    path('report/delete/', views.delete_report, name='delete_report'),

]