from django.urls import path
from . import views

urlpatterns = [
    
    path('categories', views.categories, name='categories'),
    path('add_category', views.add_category, name='add_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('update_category/<int:category_id>/', views.update_category, name='update_category'),
# ============================================================================================================================================================================================================

    path('subcategories', views.subcategories, name='subcategories'),
    path('add_subcategory', views.add_subcategory, name='add_subcategory'),
    path('delete_subcategory/<int:subcategory_id>/', views.delete_subcategory, name='delete_subcategory'),
    path('update_subcategory/<int:subcategory_id>/', views.update_subcategory, name='update_subcategory'),

# ============================================================================================================================================================================================================
    path('registered_users', views.registered_users, name='registered_users'),
    path('add_user', views.add_user, name='add_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('update_user', views.update_user, name='update_user'),

# ============================================================================================================================================================================================================
    path('product_type', views.product_type, name='product_type'),
    path('add_product_type', views.add_product_type, name='add_product_type'),
    path('delete_producttype/<int:producttype_id>/', views.delete_producttype, name='delete_producttype'),
    path('update_producttype/<int:producttype_id>/', views.update_producttype, name='update_producttype'),

# ============================================================================================================================================================================================================
    path('product_format', views.product_format, name='product_format'),
    path('add_product_format', views.add_product_format, name='add_product_format'),
    path('delete_productformat/<int:productformat_id>/', views.delete_productformat, name='delete_productformat'),
    path('update_productformat/<int:productformat_id>/', views.update_productformat, name='update_productformat'),

# ============================================================================================================================================================================================================
    path('compliance', views.compliance, name='compliance'),
    path('add_compliance', views.add_compliance, name='add_compliance'),
    path('delete_compliance/<int:compliance_id>/', views.delete_compliance, name='delete_compliance'),
    path('update_compliance/<int:compliance_id>/', views.update_compliance, name='update_compliance'),
    
    # ============================================================================================================================================================================================================
    path('product_qualities', views.product_qualities, name='product_qualities'),
    path('add_product_quality', views.add_product_quality, name='add_product_quality'),
    path('delete_product_quality/<int:product_quality_id>/', views.delete_product_quality, name='delete_product_quality'),
    path('update_product_quality/<int:product_quality_id>/', views.update_product_quality, name='update_product_quality'),
    
    # ============================================================================================================================================================================================================
    path('applications', views.applications, name='applications'),
    path('add_application', views.add_application, name='add_application'),
    path('delete_application/<int:application_id>/', views.delete_application, name='delete_application'),
    path('update_application/<int:application_id>/', views.update_application, name='update_application'),
    # ============================================================================================================================================================================================================
    path('functions', views.functions, name='functions'),
    path('add_function', views.add_function, name='add_function'),
    path('delete_function/<int:function_id>/', views.delete_function, name='delete_function'),
    path('update_function/<int:function_id>/', views.update_function, name='update_function'),
    # ============================================================================================================================================================================================================
    path('certifications', views.certifications, name='certifications'),
    path('add_certification', views.add_certification, name='add_certification'),
    path('delete_certification/<int:certification_id>/', views.delete_certification, name='delete_certification'),
    path('update_certification/<int:certification_id>/', views.update_certification, name='update_certification'),
]