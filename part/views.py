import os
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from admin_helpers.models import Ingredients
from admin_panel.views import get_user_initials
from alfamfg_formulator import settings
from part.models import PartDocument, Parts
from vendor.models import Vendor, VendorParts
from django.core.files.storage import default_storage
from django.db.models import OuterRef, Subquery, Max, Prefetch
from django.core.files.storage import FileSystemStorage

# Create your views here.

# ============================================================================================================================================================================================================

def parts_inventory(request):
    user = request.user
    initials = get_user_initials(user)

    latest_updated_at = VendorParts.objects.filter(
        part=OuterRef('part'),
        activeFlag=True
    ).values('part').annotate(
        latest_updated_at=Max('updated_at')
    ).values('latest_updated_at')

    vendor_parts_prefetch = Prefetch(
        'vendorparts_set',
        queryset=VendorParts.objects.filter(
            activeFlag=True,
            updated_at=Subquery(latest_updated_at)
        ),
        to_attr='default_vendor_parts'
    )

    parts_inventories = Parts.objects.prefetch_related(vendor_parts_prefetch).all()

    return render(request, "parts/parts_inventory.html", {
        'initials': initials,
        'parts_inventories': parts_inventories,
    })

# ============================================================================================================================================================================================================

def finished_goods(request):
    user = request.user
    initials = get_user_initials(user)

    latest_updated_at = VendorParts.objects.filter(
        part=OuterRef('part'),
        activeFlag=True
    ).values('part').annotate(
        latest_updated_at=Max('updated_at')
    ).values('latest_updated_at')

    vendor_parts_prefetch = Prefetch(
        'vendorparts_set',
        queryset=VendorParts.objects.filter(
            activeFlag=True,
            updated_at=Subquery(latest_updated_at)
        ),
        to_attr='default_vendor_parts'
    )

    parts_inventories = Parts.objects.prefetch_related(vendor_parts_prefetch).filter(inventory_category="FINISHED GOODS")

    return render(request, "parts/finished_goods.html", {
        'initials': initials,
        'parts_inventories': parts_inventories,
    })

def raw_materials(request):
    user = request.user
    initials = get_user_initials(user)

    latest_updated_at = VendorParts.objects.filter(
        part=OuterRef('part'),
        activeFlag=True
    ).values('part').annotate(
        latest_updated_at=Max('updated_at')
    ).values('latest_updated_at')

    vendor_parts_prefetch = Prefetch(
        'vendorparts_set',
        queryset=VendorParts.objects.filter(
            activeFlag=True,
            updated_at=Subquery(latest_updated_at)
        ),
        to_attr='default_vendor_parts'
    )

    parts_inventories = Parts.objects.prefetch_related(vendor_parts_prefetch).filter(inventory_category="RAW MATERIALS")

    return render(request, "parts/raw_materials.html", {
        'initials': initials,
        'parts_inventories': parts_inventories,
    })
    
def packaging(request):
    user = request.user
    initials = get_user_initials(user)

    latest_updated_at = VendorParts.objects.filter(
        part=OuterRef('part'),
        activeFlag=True
    ).values('part').annotate(
        latest_updated_at=Max('updated_at')
    ).values('latest_updated_at')

    vendor_parts_prefetch = Prefetch(
        'vendorparts_set',
        queryset=VendorParts.objects.filter(
            activeFlag=True,
            updated_at=Subquery(latest_updated_at)
        ),
        to_attr='default_vendor_parts'
    )

    parts_inventories = Parts.objects.prefetch_related(vendor_parts_prefetch).filter(inventory_category="PACKAGING")

    return render(request, "parts/packaging.html", {
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

def vendor_download(request, filename):
    file_path = os.path.join(settings.BASE_DIR, 'Vendor Pricing', filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
    else:
        raise Http404("File does not exist")
    
def upload_partdocuments(request):
    if request.method == 'POST':
        vendor = request.POST.get('vendor-readonly')
        vendorpart = request.POST.get('vendorpartnum-readonly')
        part_id = request.POST.get('part_id')  # Retrieve part_id from POST data
        vendorparts_id = request.POST.get('vendorparts_id')
        files = request.FILES.getlist('documents')
        document_type = request.POST.get('document_type')

        for f in files:
            original_extension = os.path.splitext(f.name)[1]  # e.g., .jpg, .csv

            new_filename = f"{os.path.splitext(f.name)[0]} - {vendor} - {vendorpart}{original_extension}"

            # Save the file with the custom filename
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            saved_filename = fs.save(new_filename, f)

            # Save the file information to the database
            PartDocument.objects.create(vendorparts_id=vendorparts_id, file=saved_filename, type=document_type)

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