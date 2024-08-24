from collections import defaultdict
import re
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
import csv
from django.contrib import messages
from django.contrib.auth.models import User
from admin_helpers.models import Staging
from admin_panel.models import FolderFormula, Formula, Formula_Ingredients
from part.models import Parts
from utilities.models import Category, Compliance, ProductFormat, ProductQualities, ProductType, SubCategory

# Create your views here.

# ============================================================================================================================================================================================================

def get_user_initials(user):
    
    if user.is_superuser:
        
        first_name = user.first_name
        last_name = user.last_name
        if first_name and last_name:
            initials = f"{first_name[0].upper()}{last_name[0].upper()}"
            
        else:
            initials = user.username[0].upper() if user.username else ""
    else:
        first_name = user.first_name
        last_name = user.last_name
        initials = f"{first_name[0].upper()}{last_name[0].upper()}" if first_name and last_name else ""

    return initials

# ============================================================================================================================================================================================================

def account_settings(request):

    user = request.user
    initials = get_user_initials(user)

    return render(request, "admin/account_settings.html", {
        'initials' : initials,
        'user' : user,
        'user_firstname' : user.first_name,
        'user_lastname' : user.last_name,
        'user_email' : user.email
    })

# ============================================================================================================================================================================================================

def dashboard(request):
    
    user = request.user
    initials = get_user_initials(user)
        
    return render(request, "admin/dashboard.html", {
        'initials': initials,
        'user': user,
    })

# ============================================================================================================================================================================================================

def formula(request):
    
    user = request.user
    initials = get_user_initials(user)
    folder_formulas = FolderFormula.objects.all()
    formulas = Formula.objects.all()
    allcategory = Category.objects.all()
    allsubcategory = SubCategory.objects.all()
    allproducttype = ProductType.objects.all()
    allcompliance = Compliance.objects.all()
    
    folder_formulas_with_counts = []

    for folder in folder_formulas:
        num_formulas = Formula.objects.filter(assigned_folder=folder.id).count()
        folder.num_formulas = num_formulas 
        folder_formulas_with_counts.append({
            'id': folder.id,
            'folder_name': folder.folder_name,
            'num_formulas': num_formulas,
        })
        
    return render(request, "admin/formula.html", {
        'initials': initials,
        'user': user,
        'folder_formulas' : folder_formulas,
        'formulas' : formulas,
        'folder_formulas_with_counts': folder_formulas_with_counts,
        'allcategory' : allcategory,
        'allsubcategory' : allsubcategory,
        'allproducttype' : allproducttype,
        'allcompliance' : allcompliance,

    })
    
# ============================================================================================================================================================================================================

def add_folder_formulas(request): 
    if request.method == 'POST':
        folder_name = request.POST['folder_name']
        user_id = request.POST['user_id']

        if FolderFormula.objects.filter(folder_name=folder_name).exists():
            messages.error(request, 'Folder already exists')
        else:
            folder_formula = FolderFormula(
                folder_name=folder_name,
                user_id=user_id
            )
            folder_formula.save()
            
            messages.success(request, 'Folder created successfully')
        
        return redirect(request.META['HTTP_REFERER'])

# ============================================================================================================================================================================================================

def update_folder(request):
    if request.method == 'POST':
        folder_name = request.POST['folder_name']

        folder_id = request.POST['folder_id']

        folders = get_object_or_404(FolderFormula, id=folder_id)
        folders.folder_name = folder_name
        folders.save()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    
# ============================================================================================================================================================================================================

def delete_folder(request, folder_id):
    if request.method == 'DELETE':
        folder = get_object_or_404(FolderFormula, id=folder_id)

        if folder.formulas.exists():
            messages.warning(request, "Unable to delete this folder because it has associated formulas.")
        else:
            folder.delete()
            messages.success(request, 'Folder deleted successfully')

        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request method"}, status=400)

# ============================================================================================================================================================================================================

def get_csv_formulas(request):
    if request.method == "POST":
        csv_file = request.FILES['csv_file']
        assigned_folder = request.POST['assigned_folder']
        assigned_folder_instance = get_object_or_404(FolderFormula, pk=assigned_folder)

        decoded_file = csv_file.read().decode('utf-8').splitlines() 
        csv_reader = csv.reader(decoded_file)

        for row in csv_reader:
            formula_name = row[0]  # 

            obj, created = Formula.objects.update_or_create(
                formula_name=formula_name,
                defaults={
                    'formula_name': formula_name,
                    'assigned_folder': assigned_folder_instance,
                }
            )

        return redirect(request.META['HTTP_REFERER'])
    
# ============================================================================================================================================================================================================

def delete_formula(request, formula_id):
    formula = get_object_or_404(Formula, id=formula_id)
    formula.delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

# ============================================================================================================================================================================================================

def add_formula(request):
    
        user = request.user
        initials = get_user_initials(user)
        folder_formulas = FolderFormula.objects.all()
        allcategory = Category.objects.all()
        allsubcategory = SubCategory.objects.all()
        users = User.objects.exclude(is_superuser=True)
        allproducttype = ProductType.objects.all()
        allproductformat = ProductFormat.objects.all()
        allproductqualities = ProductQualities.objects.all()
        
        return render(request, "admin/add_formula.html", {
        'initials': initials,
        'folder_formulas' : folder_formulas,
        'allcategory' : allcategory,
        'allsubcategory' : allsubcategory,
        'allproducttype' : allproducttype,
        'allproductformat' : allproductformat,
        'allproductqualities' : allproductqualities,
        'users' : users,

    })

# ============================================================================================================================================================================================================

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(category_id=category_id)
    subcategories_list = list(subcategories.values('id', 'subcategory_name'))
    print(subcategories_list)
    return JsonResponse(subcategories_list, safe=False)

def get_producttypes(request):
    subcategory_id = request.GET.get('subcategory_id')
    producttypes = ProductType.objects.filter(subcategory_id=subcategory_id)
    producttypes_list = list(producttypes.values('id', 'product_type'))
    return JsonResponse(producttypes_list, safe=False)

# ============================================================================================================================================================================================================

def create_formula(request):
    if request.method == 'POST':

        formula_name = request.POST.get('product_name')
        brand_name = request.POST.get('brand_name')
        formula_num = request.POST.get('formula_num')
        upc = request.POST.get('upc')
        assigned_folder_id = request.POST.get('folderSelect')
        category_id = request.POST.get('category-select')
        subcategory_id = request.POST.get('subcategory-select')
        product_type_id = request.POST.get('product_type')
        product_format_id = request.POST.get('product_format')
        formula_owner = request.POST.get('formula_owner')
        product_qualities_ids = request.POST.getlist('product_qualities')

        formula = Formula(
            formula_name=formula_name,
            brand_name=brand_name,
            formula_num=formula_num,
            upc=upc,
            assigned_folder_id=assigned_folder_id,
            category_id=category_id,
            subcategory_id=subcategory_id,
            product_type_id=product_type_id,
            product_format_id=product_format_id,
            formula_owner_id=formula_owner,
        )
        
        formula.save()

        if product_qualities_ids:
            formula.product_quality.set(product_qualities_ids)
            
        #return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        return redirect('/admin/formula')

# ============================================================================================================================================================================================================

def edit_formula(request, id):
    
    user = request.user
    initials = get_user_initials(user)
    
    formula = get_object_or_404(Formula, id=id)
    folder_formulas = FolderFormula.objects.all() 
    allcategory = Category.objects.all()
    allsubcategory = SubCategory.objects.all()
    allproductformat = ProductFormat.objects.all()
    product_qualities = formula.product_quality.all()
    allproductqualities = ProductQualities.objects.all()
    users = User.objects.exclude(is_superuser=True)
    ingredients = Formula_Ingredients.objects.filter(formula_id=id)
    associated_ingredients = Formula_Ingredients.objects.filter(formula=formula).order_by('staging', 'sortOrder')

    ingredients_by_stage = defaultdict(list)
    no_stage_ingredients = []

    # Process ingredients based on their staging
    for ingredient in associated_ingredients:
        if ingredient.staging and ingredient.staging.id != 1:  # Exclude staging_id 1 from stages
            print(f"Ingredient {ingredient.ingredient_name} has staging: {ingredient.staging}")
            ingredients_by_stage[ingredient.staging].append(ingredient)
        else:
            # Handle No Stage
            no_stage_ingredients.append(ingredient)
            
    formula_subcategory = {
        'subcategory_id': formula.subcategory.id,
        'subcategory_name': formula.subcategory.subcategory_name
    }
   
    formula_product_type = {
        'product_type_id' : formula.product_type.id,
        'product_type' : formula.product_type.product_type
    }
    
    formula_owner = {
        'id' : formula.formula_owner_id,
    }
       
    context = {
        'formula': formula,
        'folder_formulas': folder_formulas,
        
        'selected_folder_id': formula.assigned_folder_id,
        'selected_category_id' : formula.category_id,
        'selected_subcategory_id': formula.subcategory_id,
        'selected_product_format_id' : formula.product_format_id,
        
        'allcategory' : allcategory,
        'allsubcategory' : allsubcategory,
        'allproductformat' : allproductformat,
        'product_qualities': product_qualities,
        'allproductqualities': allproductqualities, 

        'formula_subcategory': formula_subcategory,
        'formula_product_type' : formula_product_type,
        'formula_owner' : formula_owner,
        'initials': initials,

        'users' : users,
        'ingredients' : ingredients,
        'associated_ingredients' : associated_ingredients,
        
        'ingredients_by_stage': dict(ingredients_by_stage),
        'no_stage_ingredients': no_stage_ingredients,

    }
       
    return render(request, 'admin/formula_edit.html', context) 

# ============================================================================================================================================================================================================

def update_formula(request):
    if request.method == 'POST':
        formula_id = request.POST.get('formula_id')
        formula = get_object_or_404(Formula, id=formula_id)

        formula_name = request.POST.get('product_name')
        brand_name = request.POST.get('brand_name')
        formula_num = request.POST.get('formula_num')
        upc = request.POST.get('upc')
        assigned_folder_id = request.POST.get('folderSelect')
        category_id = request.POST.get('category-select')
        subcategory_id = request.POST.get('subcategory-select')
        product_type_id = request.POST.get('product_type')
        product_format_id = request.POST.get('product_format')
        formula_owner_id = request.POST.get('formula_owner')
        product_qualities_ids = request.POST.getlist('product_qualities')

        if assigned_folder_id:
            assigned_folder_instance = get_object_or_404(FolderFormula, pk=assigned_folder_id)
            formula.assigned_folder = assigned_folder_instance

        formula.formula_name = formula_name
        formula.brand_name = brand_name
        formula.formula_num = formula_num
        formula.upc = upc
        formula.category_id = category_id
        formula.subcategory_id = subcategory_id
        formula.product_type_id = product_type_id
        formula.product_format_id = product_format_id
        formula.formula_owner_id = formula_owner_id

        formula.save()

        # Update ManyToMany field
        if product_qualities_ids:
            formula.product_quality.set(product_qualities_ids)
        else:
            formula.product_quality.clear()  # Clear the field if no qualities are provided

        return redirect('/admin/formula')
    
# ============================================================================================================================================================================================================

def add_formula_ingredient(request):
    if request.method == 'POST':
        formula_id = request.POST.get('formula_id')
        selected_parts = request.POST.getlist('ingredient_name[]')

        formula = get_object_or_404(Formula, id=formula_id)
        
        for part_id in selected_parts:
            part = get_object_or_404(Parts, id=part_id)
            formula.parts.add(part)
        
        formula.save()
        
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def delete_formula_part(request, formula_id, part_id):
    formula = get_object_or_404(Formula, id=formula_id)
    part = get_object_or_404(Parts, id=part_id)
    
    formula.parts.remove(part)
    
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

# ============================================================================================================================================================================================================
# ============================================================================================================================================================================================================

def formula_ingredient(request, formula_id):
    user = request.user
    initials = get_user_initials(user)
    formula = get_object_or_404(Formula, id=formula_id)
    
    associated_ingredients = Formula_Ingredients.objects.filter(formula=formula).order_by('staging', 'sortOrder')

    ingredient_names = '\n'.join([ing.ingredient_name for ing in associated_ingredients])

    ingredients_by_stage = defaultdict(list)
    no_stage_ingredients = []

    # Process ingredients based on their staging
    for ingredient in associated_ingredients:
        if ingredient.staging and ingredient.staging.id != 1:  # Exclude staging_id 1 from stages
            print(f"Ingredient {ingredient.ingredient_name} has staging: {ingredient.staging}")
            ingredients_by_stage[ingredient.staging].append(ingredient)
        else:
            # Handle No Stage
            no_stage_ingredients.append(ingredient)

    # Get all possible stages
    staging = Staging.objects.all()

    return render(request, "admin/formula_ingredients.html", {
        'initials': initials,
        'formula': formula,
        'ingredients_by_stage': dict(ingredients_by_stage),
        'no_stage_ingredients': no_stage_ingredients,
        'staging': staging,
        'ingredient_names': ingredient_names
    })
    
# ============================================================================================================================================================================================================

def add_ingredient(request, formula_id):
    if request.method == 'POST':
        ingredient_names = request.POST.get('ingredient_name', '').strip()

        ingredients_list = [ingredient.strip() for ingredient in re.split(r'[,\n]+', ingredient_names) if ingredient.strip()]

        formula = get_object_or_404(Formula, id=formula_id)

        Formula_Ingredients.objects.filter(formula=formula).delete()

        for idx, ingredient_name in enumerate(ingredients_list, start=1):
            Formula_Ingredients.objects.create(
                formula=formula,
                ingredient_name=ingredient_name,
                sortOrder=idx,
                staging_id=1,
            )

        formatted_ingredients = '\n'.join(ingredients_list)

        return JsonResponse({'success': True, 'formatted_ingredients': formatted_ingredients})
    else:
        return JsonResponse({'success': False}, status=400)
        
# ============================================================================================================================================================================================================

def delete_ingredient(request, id):
    ingredient = get_object_or_404(Formula_Ingredients, id=id)
    ingredient.delete()
    
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

# ============================================================================================================================================================================================================

def update_sort_order(request):
    if request.method == 'POST':
        sorted_ids = request.POST.getlist('sorted_ids[]')
        staging_id = request.POST.get('staging_id')  # This may be None for "No Stage"

        print(f"Received sorted_ids: {sorted_ids}")
        print(f"Received staging_id: {staging_id}")

        sorted_ids = list(map(int, sorted_ids))

        if staging_id is None:
            print("Handling No Stage")

            # Get IDs of ingredients with no stage
            no_stage_ingredients = Formula_Ingredients.objects.filter(staging__isnull=True)
            no_stage_ids = list(no_stage_ingredients.values_list('id', flat=True))
            print(f"Number of no stage ingredients before reset: {len(no_stage_ids)}")
            print(f"No stage ingredient IDs: {no_stage_ids}")

            # Reset sortOrder for all ingredients with no staging
            Formula_Ingredients.objects.filter(staging__isnull=True).update(sortOrder=None)

            # Update sortOrder for the new order starting from 1
            for idx, ingredient_id in enumerate(sorted_ids, start=1):
                if ingredient_id in no_stage_ids:
                    print(f"Updating ingredient_id {ingredient_id} with sortOrder {idx}.")
                    Formula_Ingredients.objects.filter(id=ingredient_id, staging__isnull=True).update(sortOrder=idx)
                else:
                    print(f"Ingredient_id {ingredient_id} not found in no stage ingredients.")

        else:
            print(f"Handling staging_id {staging_id}")

            # Get IDs of ingredients in the given staging
            staging_ingredients = Formula_Ingredients.objects.filter(staging_id=staging_id)
            staging_ids = list(staging_ingredients.values_list('id', flat=True))
            print(f"Number of staging ingredients before reset: {len(staging_ids)}")
            print(f"Staging ingredient IDs: {staging_ids}")

            # Reset sortOrder for all ingredients in the given staging
            Formula_Ingredients.objects.filter(staging_id=staging_id).update(sortOrder=None)

            # Update sortOrder for the new order starting from 1
            for idx, ingredient_id in enumerate(sorted_ids, start=1):
                if ingredient_id in staging_ids:
                    print(f"Updating ingredient_id {ingredient_id} with sortOrder {idx}.")
                    Formula_Ingredients.objects.filter(id=ingredient_id, staging_id=staging_id).update(sortOrder=idx)
                else:
                    print(f"Ingredient_id {ingredient_id} not found in stage ingredients.")

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False}, status=400)
    
# ============================================================================================================================================================================================================

def update_staging(request):
    if request.method == 'POST':
        ingredient_id = request.POST.get('ingredient_id')
        new_staging_id = request.POST.get('staging_id')  # May be None
        
        ingredient = get_object_or_404(Formula_Ingredients, id=ingredient_id)
        old_staging_id = ingredient.staging_id

        # Update the staging
        ingredient.staging_id = new_staging_id
        ingredient.save()

        # Reset and reorder sortOrder for ingredients in the old staging
        if old_staging_id or old_staging_id is None:
            Formula_Ingredients.objects.filter(staging_id=old_staging_id).update(sortOrder=None)
            for idx, ing in enumerate(Formula_Ingredients.objects.filter(staging_id=old_staging_id).order_by('sortOrder'), start=1):
                ing.sortOrder = idx
                ing.save()

        # Reset and reorder sortOrder for ingredients in the new staging
        if new_staging_id or new_staging_id is None:
            Formula_Ingredients.objects.filter(staging_id=new_staging_id).update(sortOrder=None)
            for idx, ing in enumerate(Formula_Ingredients.objects.filter(staging_id=new_staging_id).order_by('sortOrder'), start=1):
                ing.sortOrder = idx
                ing.save()

        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

# ============================================================================================================================================================================================================
# ============================================================================================================================================================================================================
