from io import BytesIO
import os
from django.http import FileResponse, Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from openpyxl import Workbook
import json
from django.urls import reverse
from admin_panel.models import Formula
from admin_panel.views import get_user_initials
from alfamfg_formulator import settings
from reports.models import Generated_Reports

def generate_excel_report(request):
    if request.method == 'POST':

        formula_ids = request.POST.get('formula_ids', '[]')
        formula_ids = json.loads(formula_ids)
        formula_ids = list(map(int, formula_ids))

        formulas = Formula.objects.filter(id__in=formula_ids).select_related(
            'assigned_folder', 'category', 'subcategory', 'product_type', 'product_format', 'formula_owner'
        ).prefetch_related('product_quality', 'parts', 'formula_ingredients_set')

        wb = Workbook()
        ws = wb.active
        ws.title = "Formulas Report"

        headers = [
            "Folder", "Formula Name", "Brand Name", "Formula Number",
            "Category", "Subcategory", "Product Type", "Product Format", "Formula Owner", "Product Qualities", 
            "Ingredient Name"
        ]
        ws.append(headers)

        formula_names = set() 

        for formula in formulas:
            formula_names.add(formula.formula_num)

            base_row = [
                formula.assigned_folder.folder_name if formula.assigned_folder else '',
                formula.formula_name or '',
                formula.brand_name or '',
                formula.formula_num or '',
                formula.category.category_name if formula.category else '',
                formula.subcategory.subcategory_name if formula.subcategory else '',
                formula.product_type.product_type if formula.product_type else '',
                formula.product_format.product_format if formula.product_format else '',
                f"{formula.formula_owner.first_name} {formula.formula_owner.last_name}" if formula.formula_owner else '',
                ', '.join([pq.product_quality for pq in formula.product_quality.all()]),
               # ', '.join([part.part_name for part in formula.parts.all()])
            ]

            for ingredient in formula.formula_ingredients_set.all():
                ws.append(base_row + [
                    ingredient.ingredient_name or '',
                ])

        if formula_names:
            report_name = f"Formula Codes {'-'.join(formula_names)[:100]}.xlsx"
        else:
            report_name = "Formulas_Report"
        
        reports_dir = os.path.join(settings.BASE_DIR, 'Generated Reports')
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        file_path = os.path.join(reports_dir, report_name)
    
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)
                
        with open(file_path, 'wb') as f:
            f.write(buffer.getvalue())
        
        report = Generated_Reports.objects.create(
            report_name=report_name
        )
                
        file_url = reverse('serve_report', kwargs={'filename': report_name})
        
        return JsonResponse({'success': True, 'file_url': file_url})

        """
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        print(f"Generated report name: {report_name}")

        response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{report_name}.xlsx"'
        
        return response
        """

    return JsonResponse({'success': False}, status=400)

def serve_report(request, filename):
    file_path = os.path.join(settings.BASE_DIR, 'Generated Reports', filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
    else:
        raise Http404("File does not exist")
    
def generated_reports(request):
    
    user = request.user
    initials = get_user_initials(user)
    generated_report = Generated_Reports.objects.all()
    
    return render(request, "admin/generated_reports.html", {
        'initials': initials,
        'generated_reports': generated_report,

    })

def delete_report(request):
    if request.method == 'POST':
        report_id = request.POST.get('report_id')
        
        if not report_id:
            return HttpResponseBadRequest("No report ID provided")
        
        try:
            report = Generated_Reports.objects.get(id=report_id)
            file_path = os.path.join(settings.BASE_DIR, 'Generated Reports', report.report_name)
            
            if os.path.exists(file_path):
                os.remove(file_path)
            
            report.delete()
            return JsonResponse({'success': True})
        except Generated_Reports.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Report not found'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)