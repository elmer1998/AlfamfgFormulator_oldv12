from django.urls import path
from . import views

urlpatterns = [
    
# ============================================================================================================================================================================================================
    path('vendors', views.vendors, name='vendors'),
    path('add_vendor', views.add_vendor, name='add_vendor'),
    path('delete_vendor/<int:id>/', views.delete_vendor, name='delete_vendor'),
    path('update_vendor', views.update_vendor, name='update_vendor'),

# ============================================================================================================================================================================================================
    path('add_vendorparts', views.add_vendorparts, name='add_vendorparts'),
    path('delete_vendorparts/<int:id>/', views.delete_vendorparts, name='delete_vendorparts'),

]