from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.hashers import make_password
from admin_panel.views import get_user_initials
from utilities.models import Applications, Category, Certifications, Compliance, Functions, ProductFormat, ProductQualities, ProductType, SubCategory
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

def categories(request):

    user = request.user
    initials = get_user_initials(user)
    categories = Category.objects.all()
    
    return render(request, "utilities/category.html", {
        'initials' : initials,
        'user' : user,
        'user_firstname' : user.first_name,
        'user_lastname' : user.last_name,
        'user_email' : user.email,
        'categories' : categories
    })
    
#====================================================================================================================================================================================

def add_category(request):
    
    if request.method == 'POST':
        category_name = request.POST['category_name']

        if Category.objects.filter(category_name=category_name).exists():
            messages.error(request, 'Category already exists')
        else:
            category = Category(
                category_name=category_name,
            )
            category.save()
                    
        return redirect(request.META['HTTP_REFERER'])

#====================================================================================================================================================================================

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

#====================================================================================================================================================================================

def update_category(request, category_id):
    if request.method == 'POST':
        category_name = request.POST['category_name']

        category = get_object_or_404(Category, id=category_id)
        category.category_name = category_name
        category.save()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

#====================================================================================================================================================================================
#====================================================================================================================================================================================

def subcategories(request):

    user = request.user
    initials = get_user_initials(user)
    categories = Category.objects.all()

    #subcategories = SubCategory.objects.all()
    subcategories = SubCategory.objects.select_related('category').all()

    return render(request, "utilities/subcategory.html", {
        'initials' : initials,
        'user' : user,
        'user_firstname' : user.first_name,
        'user_lastname' : user.last_name,
        'user_email' : user.email,
        'subcategories' : subcategories,
        'categories' : categories

    })
    
#====================================================================================================================================================================================

def add_subcategory(request):
    
    if request.method == 'POST':
        subcategory_name = request.POST['subcategory_name']
        category_id = request.POST['category_id']
        
        if SubCategory.objects.filter(subcategory_name=subcategory_name).exists():
            messages.error(request, 'SubCategory already exists')
        else:
            subcategory = SubCategory(
                subcategory_name=subcategory_name,
                category_id=category_id,
            )
            
            subcategory.save()
                    
        return redirect(request.META['HTTP_REFERER'])
    
#====================================================================================================================================================================================

def delete_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    subcategory.delete()
    
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

#====================================================================================================================================================================================

def update_subcategory(request, subcategory_id):
    if request.method == 'POST':
        subcategory = get_object_or_404(SubCategory, id=subcategory_id)

        subcategory_name = request.POST.get('subcategory_name')
        category_id = request.POST.get('category_id')

        try:
            category_id = int(category_id)
        except ValueError:
            return JsonResponse({'error': 'Invalid category ID'}, status=400)
        
        subcategory.subcategory_name = subcategory_name
        subcategory.category_id = category_id
        subcategory.save()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

#====================================================================================================================================================================================
#============================================================================================================================================================================================================

def registered_users(request):
    
    user = request.user
    initials = get_user_initials(user)

    all_users = User.objects.exclude(is_superuser=True)
    user_data = []

    for user in all_users:
        user_initials = get_user_initials(user)
        status = "Approved" if user.is_active else "Not Approved"

        user_data.append({
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email' : user.email,
            'last_login' : user.last_login.astimezone(timezone.get_current_timezone()) if user.last_login else None,
            'date_joined' : user.date_joined,
            'user_initials': user_initials,
            'status': status,
        })

    return render(request, "utilities/users.html", {
        'initials': initials,
        'user_data': user_data,
        'user_firstname' : user.first_name,
        'user_lastname' : user.last_name,
        'user_email' : user.email

    })

# ============================================================================================================================================================================================================

def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

        new_user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=make_password(password), 
            is_active=True  
        )
        
        new_user.save() 
        messages.success(request, 'User added successfully.')
        
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

#============================================================================================================================================================================================================

def delete_user(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)
    user_to_delete.delete()
    
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

#============================================================================================================================================================================================================

def update_user(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        user_id = request.POST['user_id']
        status = request.POST['status']

        updateuser = get_object_or_404(User, id=user_id)
        updateuser.first_name = first_name
        updateuser.last_name = last_name
        updateuser.username = username
        
        if status == 'Approved':
            updateuser.is_active = True
        else:
            updateuser.is_active = False        
        
        updateuser.email = email

        updateuser.save()
        messages.success(request, "Updated Successfully")

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    
    # ============================================================================================================================================================================================================

#====================================================================================================================================================================================
#============================================================================================================================================================================================================

def product_type(request):

    user = request.user
    initials = get_user_initials(user)
    
    subcategories = SubCategory.objects.all()

    #subcategories = SubCategory.objects.all()
    product_types = ProductType.objects.select_related('subcategory').all()  # Use select_related for efficient querying

    return render(request, "utilities/product_type.html", {
        'initials' : initials,
        'user' : user,
        'user_firstname' : user.first_name,
        'user_lastname' : user.last_name,
        'user_email' : user.email,
        'product_types' : product_types,
        'subcategories' : subcategories

    })

#============================================================================================================================================================================================================

def add_product_type(request):
    
    if request.method == 'POST':
        product_type = request.POST['product_type']
        subcategory_id = request.POST['subcategory_id']
        
        if ProductType.objects.filter(product_type=product_type).exists():
            messages.error(request, 'Product Type already exists')
        else:
            product_types = ProductType(
                product_type=product_type,
                subcategory_id=subcategory_id,
            )
            
            product_types.save()
                    
        return redirect(request.META['HTTP_REFERER'])

#============================================================================================================================================================================================================ 

def delete_producttype(request, producttype_id):
    product_type = get_object_or_404(ProductType, id=producttype_id)
    product_type.delete()
    
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

#====================================================================================================================================================================================

def update_producttype(request, producttype_id):
    if request.method == 'POST':
        product_types = get_object_or_404(ProductType, id=producttype_id)

        product_type = request.POST.get('product_type')
        subcategory_id = request.POST.get('subcategory_id')

        try:
            subcategory_id = int(subcategory_id)
        except ValueError:
            return JsonResponse({'error': 'Invalid subcategory ID'}, status=400)
        
        product_types.product_type = product_type
        product_types.subcategory_id = subcategory_id
        product_types.save()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    
#====================================================================================================================================================================================
#====================================================================================================================================================================================

def product_format(request):

    user = request.user
    initials = get_user_initials(user)
    
    product_formats = ProductFormat.objects.all()

    return render(request, "utilities/product_format.html", {
        'initials' : initials,
        'user' : user,
        'user_firstname' : user.first_name,
        'user_lastname' : user.last_name,
        'user_email' : user.email,
        'product_formats' : product_formats,

    })

#====================================================================================================================================================================================

def add_product_format(request):
    
    if request.method == 'POST':
        product_format = request.POST['product_format']
        
        if ProductFormat.objects.filter(product_format=product_format).exists():
            messages.error(request, 'Product Format already exists')
        else:
            product_formats = ProductFormat(
                product_format=product_format,
            )
            
            product_formats.save()
                    
        return redirect(request.META['HTTP_REFERER'])

#============================================================================================================================================================================================================ 

def delete_productformat(request, productformat_id):
    product_format = get_object_or_404(ProductFormat, id=productformat_id)
    product_format.delete()
    
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

#====================================================================================================================================================================================

def update_productformat(request, productformat_id):
    if request.method == 'POST':
        
        product_formats = get_object_or_404(ProductFormat, id=productformat_id)
        product_format = request.POST.get('product_format')
        
        product_formats.product_format = product_format
        product_formats.save()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    
#====================================================================================================================================================================================
#====================================================================================================================================================================================

def compliance(request):

    user = request.user
    initials = get_user_initials(user)
    
    compliances = Compliance.objects.all()

    return render(request, "utilities/compliance.html", {
        'initials' : initials,
        'user' : user,
        'user_firstname' : user.first_name,
        'user_lastname' : user.last_name,
        'user_email' : user.email,
        'compliances' : compliances,

    })

#====================================================================================================================================================================================
def add_compliance(request):
    
    if request.method == 'POST':
        compliance = request.POST['compliance']
        
        if Compliance.objects.filter(compliance=compliance).exists():
            messages.error(request, 'Compliance already exists')
        else:
            compliances = Compliance(
                compliance=compliance,
            )
            
            compliances.save()
                    
        return redirect(request.META['HTTP_REFERER'])

#============================================================================================================================================================================================================ 
def delete_compliance(request, compliance_id):
    compliance = get_object_or_404(Compliance, id=compliance_id)
    compliance.delete()
    
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

#====================================================================================================================================================================================

def update_compliance(request, compliance_id):
    if request.method == 'POST':
        
        compliances = get_object_or_404(Compliance, id=compliance_id)
        compliance = request.POST.get('compliance')
        
        compliances.compliance = compliance
        compliances.save()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

#====================================================================================================================================================================================
#====================================================================================================================================================================================

def product_qualities(request):

    user = request.user
    initials = get_user_initials(user)
    
    product_qualities = ProductQualities.objects.all()

    return render(request, "utilities/product_qualities.html", {
        'initials' : initials,
        'user' : user,
        'user_firstname' : user.first_name,
        'user_lastname' : user.last_name,
        'user_email' : user.email,
        'product_qualities' : product_qualities,

    })

#====================================================================================================================================================================================
def add_product_quality(request):
    
    if request.method == 'POST':
        product_quality = request.POST['product_quality']
        
        if ProductQualities.objects.filter(product_quality=product_quality).exists():
            messages.error(request, 'Product Quality already exists')
        else:
            product_qualities = ProductQualities(
                product_quality=product_quality,
            )
            
            product_qualities.save()
                    
        return redirect(request.META['HTTP_REFERER'])

#============================================================================================================================================================================================================ 
def delete_product_quality(request, product_quality_id):
    product_quality = get_object_or_404(ProductQualities, id=product_quality_id)
    product_quality.delete()
    
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

#====================================================================================================================================================================================

def update_product_quality(request, product_quality_id):
    if request.method == 'POST':
        
        product_qualitys = get_object_or_404(ProductQualities, id=product_quality_id)
        product_quality = request.POST.get('product_quality')
        
        product_qualitys.product_quality = product_quality
        product_qualitys.save()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

#====================================================================================================================================================================================

def applications(request):
    
    user = request.user
    initials = get_user_initials(user)
    
    applications = Applications.objects.all()

    return render(request, "utilities/applications.html", {
        'initials' : initials,
        'user' : user,
        'applications' : applications,

    })
    
#====================================================================================================================================================================================
def add_application(request):
    
    if request.method == 'POST':
        application = request.POST['application']
        
        if Applications.objects.filter(applications=application).exists():
            messages.error(request, 'Application already exists')
        else:
            applications = Applications(
                applications=application,
            )
            
            applications.save()
                    
        return redirect(request.META['HTTP_REFERER'])

#============================================================================================================================================================================================================ 
def delete_application(request, application_id):
    application = get_object_or_404(Applications, id=application_id)
    application.delete()
    
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

#====================================================================================================================================================================================

def update_application(request, application_id):
    if request.method == 'POST':
        
        applications = get_object_or_404(Applications, id=application_id)
        application = request.POST.get('applications')
        
        applications.applications = application
        applications.save()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

#====================================================================================================================================================================================

def functions(request):
    
    user = request.user
    initials = get_user_initials(user)
    
    functions = Functions.objects.all()

    return render(request, "utilities/functions.html", {
        'initials' : initials,
        'user' : user,
        'functions' : functions,

    })
    
#====================================================================================================================================================================================
def add_function(request):
    
    if request.method == 'POST':
        function = request.POST['functions']
        
        if Functions.objects.filter(functions=function).exists():
            messages.error(request, 'Function already exists')
        else:
            functions = Functions(
                functions=function,
            )
            
            functions.save()
                    
        return redirect(request.META['HTTP_REFERER'])

#============================================================================================================================================================================================================ 
def delete_function(request, function_id):
    function = get_object_or_404(Functions, id=function_id)
    function.delete()
    
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

#====================================================================================================================================================================================

def update_function(request, function_id):
    if request.method == 'POST':
        
        functions = get_object_or_404(Functions, id=function_id)
        function = request.POST.get('functions')
        
        functions.functions = function
        functions.save()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

#====================================================================================================================================================================================

def certifications(request):
    
    user = request.user
    initials = get_user_initials(user)
    
    certifications = Certifications.objects.all()

    return render(request, "utilities/certifications.html", {
        'initials' : initials,
        'user' : user,
        'certifications' : certifications,

    })
    
#====================================================================================================================================================================================
def add_certification(request):
    
    if request.method == 'POST':
        certification = request.POST['certifications']
        
        if Certifications.objects.filter(certifications=certification).exists():
            messages.error(request, 'Certification already exists')
        else:
            certifications = Certifications(
                certifications=certification,
            )
            
            certifications.save()
                    
        return redirect(request.META['HTTP_REFERER'])

#============================================================================================================================================================================================================ 
def delete_certification(request, certification_id):
    certification = get_object_or_404(Certifications, id=certification_id)
    certification.delete()
    
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

#====================================================================================================================================================================================

def update_certification(request, certification_id):
    if request.method == 'POST':
        
        certifications = get_object_or_404(Certifications, id=certification_id)
        certification = request.POST.get('certifications')
        
        certifications.certifications = certification
        certifications.save()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

#====================================================================================================================================================================================
