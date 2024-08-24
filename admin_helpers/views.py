from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from part.models import PartDocument, Parts
from vendor.models import Vendor, VendorParts

# Create your views here.

def add_document_view(request, vendorparts_id):
    # Get the specific vendor part
    vendor_part = get_object_or_404(VendorParts, id=vendorparts_id)
    print(f"Vendor Part ID: {vendor_part.id}")

    # Get all document types already associated with this vendor part
    existing_document_types = PartDocument.objects.filter(vendorparts_id=vendor_part).values_list('type', flat=True)
    print(f"Existing Document Types for Vendor Part {vendor_part.id}: {list(existing_document_types)}")

    # Define all possible document types
    all_document_types = [
        'Technical Data Sheet',
        'Safety Data Sheet (SDS)',
        'Material Questionnaire',
        'Composition Statement',
        'No Animal Testing'
    ]
    
    # Exclude the document types that are already associated with this vendor part
    available_document_types = [doc_type for doc_type in all_document_types if doc_type not in existing_document_types]
    print(f"Available Document Types for Vendor Part {vendor_part.id}: {available_document_types}")

    # Return the available document types as a JSON response
    return JsonResponse({'available_document_types': available_document_types})

# ============================================================================================================================================================================================================
#part main retreiving the associated vendor
def part_vendor(request, part_id):
    try:
        part = get_object_or_404(Parts, id=part_id)
        vendor_parts = VendorParts.objects.filter(part=part).select_related('vendor')

        vendor_parts_list = []

        for vp in vendor_parts:
            # Retrieve related PartDocuments for each VendorPart
            part_documents = PartDocument.objects.filter(vendorparts_id=vp).values('id', 'type', 'file')
            
            # Construct the dictionary for each VendorPart
            vendor_part_data = {
                'vendor_id': vp.id,
                'vendor_name': vp.vendor.vendor_name,
                'lastcost': vp.lastcost,
                'vendor_partnum': vp.vendorPartNumber,
                'status': vp.status,
                'leadtime': vp.leadTime,
                'documents': list(part_documents)  # Convert queryset to list
            }

            vendor_parts_list.append(vendor_part_data)

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