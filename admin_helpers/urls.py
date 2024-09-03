from django.urls import path
from . import views

urlpatterns = [
    path('part_vendor/<int:part_id>/', views.part_vendor, name='part_vendor'),
    path('get_specific_vendor_by_part/<int:part_id>/', views.get_specific_vendor_by_part, name='get_specific_vendor_by_part'),
    path('vendor_parts/<int:vendor_id>/', views.vendor_parts, name='vendor_parts'),
    path('get_available_vendors_for_specific_parts', views.get_available_vendors_for_specific_parts, name='get_available_vendors_for_specific_parts'),
    path('add-document/<int:vendor_id>/', views.add_document_view, name='add_document_view'),

]