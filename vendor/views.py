
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from admin_panel.views import get_user_initials
from part.models import Parts
from vendor.models import Vendor, VendorParts

# Create your views here.

# ============================================================================================================================================================================================================

def vendors(request):

    user = request.user
    initials = get_user_initials(user)
    vendors = Vendor.objects.all()
    vendorparts = VendorParts.objects.select_related('vendor', 'part').all()
    parts = Parts.objects.all()
    
    return render(request, "admin/vendors.html", {
        'initials': initials,
        'vendors': vendors,
        'vendorparts': vendorparts,
        'parts': parts,

    })

# ============================================================================================================================================================================================================

def add_vendor(request):
    if request.method == 'POST':
        vendor_name = request.POST.get('vendor')
        default = request.POST.get('default') == 'true'
        user_id = request.POST.get('userId')

        vendors = Vendor.objects.create(
            vendor_name=vendor_name,
            default = default,
            user_id = user_id
        )
        
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

# ============================================================================================================================================================================================================

def delete_vendor(request, id):
    try:
        vendor = get_object_or_404(Vendor, id=id)
        vendor.delete()

    except Exception as e:
        print(f"Error deleting vendor: {e}")
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

# ============================================================================================================================================================================================================

def update_vendor(request):
    if request.method == 'POST':
        vendor_name = request.POST['vendor_name']
        default = request.POST['default'] == 'true'
        vendor_id = request.POST['vendor_id']
        user_id = request.POST.get('userId')

        vendors = get_object_or_404(Vendor, id=vendor_id)
        vendors.vendor_name = vendor_name
        vendors.default = default
        vendors.user_id = user_id

        vendors.save()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def update_vendor_type(request):
    if request.method == 'POST':
        vendor_id = request.POST.get('vendor_id')
        vendor_type = request.POST.get('vendor_type')

        try:
            vendor = Vendor.objects.get(id=vendor_id)
            vendor.vendor_type = vendor_type
            vendor.save()

            return JsonResponse({'status': 'success', 'message': 'Vendor type updated successfully', 'vendor_type': vendor.vendor_type})
        except Vendor.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Vendor not found'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

    
# ============================================================================================================================================================================================================
# ============================================================================================================================================================================================================

def add_vendorparts(request):
    
    if request.method == 'POST':
        #vendor_partnum = request.POST.get('vendor_partnum')
        lastcost = request.POST.get('lastcost')
        vendor_id = request.POST.get('vendor_id')
        part_id = request.POST.get('part_id')
        user_id = request.POST.get('userId')

        vendors = VendorParts.objects.create(
            #vendor_partnum=vendor_partnum,
            lastcost=lastcost,
            vendor_id=vendor_id,
            part_id=part_id,
            user_id=user_id,
        )
    
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

# ============================================================================================================================================================================================================

def delete_vendorparts(request, id):
    
    vendorparts = get_object_or_404(VendorParts, id=id)
    vendorparts.delete()

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

# ============================================================================================================================================================================================================
