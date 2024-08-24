from django.urls import path

from alfamfg_formulator import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    
    path('account_settings', views.account_settings, name='account_settings'),

# ============================================================================================================================================================================================================
    path('dashboard', views.dashboard, name='dashboard'),
    path('add_folder_formulas', views.add_folder_formulas, name='add_folder_formulas'),
    path('update_folder', views.update_folder, name='update_folder'),
    path('delete_folder/<int:folder_id>/', views.delete_folder, name='delete_folder'),
# ============================================================================================================================================================================================================
    path('formula', views.formula, name='formula'),
    path('get_csv_formulas', views.get_csv_formulas, name='get_csv_formulas'),
    #path('update_formula', views.update_formula, name='update_formula'),
    path('delete_formula/<int:formula_id>/', views.delete_formula, name='delete_formula'),

# ============================================================================================================================================================================================================
    path('add_formula', views.add_formula, name='add_formula'),
    path('create_formula', views.create_formula, name='create_formula'),
    path('edit_formula/<int:id>', views.edit_formula, name='edit_formula'),
    path('update_formula', views.update_formula, name='update_formula'),

# ============================================================================================================================================================================================================

# ============================================================================================================================================================================================================
    path('formula/<int:formula_id>/ingredient', views.formula_ingredient, name='formula_ingredient'),
    path('add_ingredient/<int:formula_id>', views.add_ingredient, name='add_ingredient'),
    path('delete_ingredient/<int:id>/', views.delete_ingredient, name='delete_ingredient'),
    path('update-sort-order/', views.update_sort_order, name='update_sort_order'),
    path('update_staging', views.update_staging, name='update_staging'),

    path('add_formula_ingredient', views.add_formula_ingredient, name='add_formula_ingredient'),
    path('delete_formula_part/<int:formula_id>/<int:part_id>/', views.delete_formula_part, name='delete_formula_part'),

# ============================================================================================================================================================================================================
    path('get_subcategories', views.get_subcategories, name='get_subcategories'),
    path('get_producttypes', views.get_producttypes, name='get_producttypes'),
# ============================================================================================================================================================================================================

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)