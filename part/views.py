import os
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from admin_helpers.models import Ingredients
from admin_panel.views import get_user_initials
from part.models import PartDocument, Parts
from vendor.models import Vendor
from django.core.files.storage import default_storage

# Create your views here.

# ============================================================================================================================================================================================================

def parts_inventory(request):
    
    user = request.user
    initials = get_user_initials(user)

    parts_inventories = Parts.objects.all()
    
    return render(request, "admin/parts_inventory.html", {
        'initials': initials,
        'parts_inventories': parts_inventories,

    })
    
# ============================================================================================================================================================================================================

def add_part(request):
    if request.method == 'POST':
        reference_number = request.POST.get('reference_number')
        description = request.POST.get('description')
        supplier_name = request.POST.get('supplier_name')
        priceper = request.POST.get('priceper')
        inventory_category = request.POST.get('inventory_category')
        num = request.POST.get('part_num')
        std_cost = request.POST.get('current_cost')
        manufacturer_name = request.POST.get('manufacturer_name')
        notes = request.POST.get('notes')
        user_id = request.POST.get('user_id')

        part = Parts.objects.create(
            reference_number=reference_number,
            description=description,
            supplier_name=supplier_name,
            priceper=priceper,
            inventory_category=inventory_category,
            num=num,
            manufacturer_name=manufacturer_name,
            notes=notes,
            std_cost=std_cost,
            user_id=user_id
        )

    """
        if(inventory_category == 'FINISHED GOODS'):
            return redirect('/parts/finished_goods')
        elif(inventory_category == 'RAW MATERIALS'):
            return redirect('/parts/raw_materials')
        else:
            return redirect('/parts/packaging')
    """
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

# ============================================================================================================================================================================================================

def update_parts(request):
    if request.method == 'POST':
        part_id = request.POST['part_id']
        num = request.POST['num']
        description = request.POST['description']
        inventory_category = request.POST['inventory_category']
        manufacturer_name = request.POST['manufacturer_name']
        notes = request.POST['notes']
        std_cost = request.POST['current_cost']
        user_id = request.POST['user_id']

        parts = get_object_or_404(Parts, id=part_id)
        parts.num = num
        parts.description = description
        parts.inventory_category=inventory_category
        parts.manufacturer_name = manufacturer_name
        parts.notes = notes
        parts.user_id = user_id
        parts.std_cost = std_cost

        parts.save()

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

# ============================================================================================================================================================================================================

def upload_partdocuments(request):
    if request.method == 'POST':
        vendorparts_id = request.POST.get('vendorparts_id')
        files = request.FILES.getlist('documents')
        type = request.POST.get('document_type')

        for f in files:
            file_name = default_storage.save(f.name, f)
            
            PartDocument.objects.create(vendorparts_id=vendorparts_id, file=file_name, type=type)

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def delete_part_document(request, document_id):
    document = get_object_or_404(PartDocument, id=document_id)
    
    file_path = document.file.path

    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File deleted: {file_path}")
    else:
        print(f"File not found: {file_path}")

    document.delete()

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

# ============================================================================================================================================================================================================

def delete_part(request, id):
  
    part = get_object_or_404(Parts, id=id)
    part.delete()

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

# ============================================================================================================================================================================================================

def delete_document(request, id):
  
    document = get_object_or_404(PartDocument, id=id)
    document.delete()

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

# ============================================================================================================================================================================================================

def add_part_ingredients(request):
    if request.method == 'POST':
        part_id = request.POST.get('part_id')
        ingredient_name = request.POST.get('ingredients')
        ingredient_type = request.POST.get('type')

        part = Parts.objects.get(id=part_id)
        
        ingredient = Ingredients.objects.create(
            name=ingredient_name,
            type=ingredient_type,
            part=part,
            user=request.user
        )

        return JsonResponse({'status': 'success', 'ingredient_id': ingredient.id, 'name': ingredient.name})
    
    return JsonResponse({'status': 'error'}, status=400)

# ============================================================================================================================================================================================================

def get_inci_name(request, part_id):
    part = get_object_or_404(Parts, id=part_id)
    ingredients = Ingredients.objects.filter(part=part, type="INCI Name").values('id', 'name', 'description')

    return JsonResponse(list(ingredients), safe=False)

def get_allergens(request, part_id):
    part = get_object_or_404(Parts, id=part_id)
    ingredients = Ingredients.objects.filter(part=part, type="Allergens").values('id', 'name', 'description')

    return JsonResponse(list(ingredients), safe=False)

def get_impurities(request, part_id):
    part = get_object_or_404(Parts, id=part_id)
    ingredients = Ingredients.objects.filter(part=part, type="Impurities").values('id', 'name', 'description')

    return JsonResponse(list(ingredients), safe=False)

# ============================================================================================================================================================================================================

def delete_ingredients(request, id):
  
    document = get_object_or_404(Ingredients, id=id)
    document.delete()

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))