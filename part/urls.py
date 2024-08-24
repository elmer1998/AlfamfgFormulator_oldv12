
from django.urls import path

from alfamfg_formulator import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
# ============================================================================================================================================================================================================
    path('parts_inventory', views.parts_inventory, name='parts_inventory'),
# ============================================================================================================================================================================================================
    path('add_part', views.add_part, name='add_part'),
    path('update_parts', views.update_parts, name='update_parts'),
    path('delete_part/<int:id>/', views.delete_part, name='delete_part'),
# ============================================================================================================================================================================================================
    path('upload_partdocuments', views.upload_partdocuments, name='upload_partdocuments'),
    path('delete_part_document/<int:document_id>/', views.delete_part_document, name='delete_part_document'),
    path('delete_document/<int:id>/', views.delete_document, name='delete_document'),
# ============================================================================================================================================================================================================
    path('add_part_ingredients', views.add_part_ingredients, name='add_part_ingredients'),
    path('part/<int:part_id>/ingredients/inci_name', views.get_inci_name, name='get_inci_name'),
    path('part/<int:part_id>/ingredients/allergens', views.get_allergens, name='get_allergens'),
    path('part/<int:part_id>/ingredients/impurities', views.get_impurities, name='get_impurities'),
    path('delete_ingredients/<int:id>/', views.delete_ingredients, name='delete_ingredients'),
# ============================================================================================================================================================================================================

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)