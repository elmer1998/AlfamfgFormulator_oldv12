from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from collections import OrderedDict
from part.models import PartDocument, Parts
from vendor.models import Vendor, VendorParts

# Create your views here.

def add_document_view(request, vendor_id):

    #vendor_part = get_object_or_404(VendorParts, id=vendorparts_id)
    vendor = get_object_or_404(Vendor, id=vendor_id)
    
    # Get all document types already associated with this vendor part
    existing_document_types = PartDocument.objects.filter(vendor_id=vendor).values_list('type', flat=True)
    print(f"Existing Document Types for Vendor Part {vendor.id}: {list(existing_document_types)}")

    all_document_types = [
        'Technical Data Sheet',
        'Safety Data Sheet (SDS)',
        'Material Questionnaire',
        'Composition Statement',
        'No Animal Testing'
    ]
    
    available_document_types = [doc_type for doc_type in all_document_types if doc_type not in existing_document_types]

    return JsonResponse({'available_document_types': available_document_types})

# ============================================================================================================================================================================================================
#part main retreiving the associated vendor
def part_vendor(request, part_id):
    try:
        part = get_object_or_404(Parts, id=part_id)
        vendor_parts = VendorParts.objects.filter(part=part).select_related('vendor', 'part')
        vendor_parts_list = []

        for vp in vendor_parts:
            
            vendor_part_data = {
                'vendorparts_id': vp.id,
                'vendor_name': vp.vendor.vendor_name,
                'lastcost': vp.lastcost,
                'vendorpartnum': vp.vendorPartNumber,
                'vendorparts_status': vp.status,
                'leadtime': vp.leadTime,
                'vendor_type': vp.vendor.vendor_type,
                'part_id' : vp.part.id,
               # 'documents': list(part_documents)
            }

            vendor_parts_list.append(vendor_part_data)

        return JsonResponse(vendor_parts_list, safe=False)
    except Parts.DoesNotExist:
        return JsonResponse({'error': 'Part not found.'}, status=404)
# ============================================================================================================================================================================================================

def get_specific_vendor_by_part(request, part_id):
    try:
        part = get_object_or_404(Parts, id=part_id)

        vendor_parts = VendorParts.objects.filter(part=part).select_related('vendor')

        unique_vendors = OrderedDict()

        for vp in vendor_parts:
            vendor_id = vp.vendor.id
            part_documents = PartDocument.objects.filter(part_id=part_id).values('id', 'type', 'file', 'status', 'notes')

            if vendor_id not in unique_vendors:
                
                vendor_part_data = {
                    'part_id': part.id,
                    'vendor_id': vp.vendor.id,
                    'vendor_name': vp.vendor.vendor_name,
                    'vendor_type': vp.vendor.vendor_type,
                    'documents': list(part_documents)

                }
                
                unique_vendors[vendor_id] = vendor_part_data

        vendor_parts_list = list(unique_vendors.values())
        print(f"Final unique vendor parts list: {vendor_parts_list}")

        return JsonResponse(vendor_parts_list, safe=False)
    except Parts.DoesNotExist:
        return JsonResponse({'error': 'Part not found.'}, status=404)
    
# ============================================================================================================================================================================================================
#vendor main retreiving the associated parts
def vendor_parts(request, vendor_id):
    try:
        vendor = get_object_or_404(Vendor, id=vendor_id)
        vendor_parts = VendorParts.objects.filter(vendor=vendor).select_related('part')

        parts_vendor_list = [
            {
                'id': vendor_part.id,
                'part_num': vendor_part.part.part_num,
                'trade_name': vendor_part.part.trade_name,
                'lastcost': vendor_part.lastcost,
                'description': vendor_part.part.description,
                'vendor_partnum': vendor_part.vendorPartNumber,
                'vendorpart_activeFlag': vendor_part.activeFlag,
                'vendorparts_leadtime': vendor_part.leadTime,

            }
            for vendor_part in vendor_parts
        ]

        return JsonResponse(parts_vendor_list, safe=False)
    except Parts.DoesNotExist:
        return JsonResponse({'error': 'Part not found.'}, status=404)

# ============================================================================================================================================================================================================

def get_available_vendors_for_specific_parts(request):
    part_id = request.GET.get('part_id')
    
    if part_id:
        associated_vendor_ids = VendorParts.objects.filter(part_id=part_id).values_list('vendor_id', flat=True).distinct()
        available_vendors = Vendor.objects.exclude(id__in=associated_vendor_ids)
        
        vendor_data = [{'id': vendor.id, 'vendor_name': vendor.vendor_name} for vendor in available_vendors]
        return JsonResponse({'vendors': vendor_data})
    
    return JsonResponse({'vendors': []})